import os
import os.path
import sys
from docxtpl import DocxTemplate, RichText
# from databasecreate import CreateDB
# from win32api import ShellExecute
# from win32print import GetDefaultPrinter


class CreateFile:
	def __init__(self, cont_dict):
		self.path_dir_temp = os.path.join(os.getcwd(), 'template')
		self.path_dir_order_file = os.path.join(os.getcwd(), 'OrderBDFile')
		self.exists_file(self.path_dir_temp)
		self.exists_file(self.path_dir_order_file)
		self.template = (
			(os.path.join(self.path_dir_temp, 'act_repair.docx'), cont_dict['chk_state'][0], 'act_repair'),
			(os.path.join(self.path_dir_temp, 'act_work.docx'), cont_dict['chk_state'][1], 'act_work'),
			(os.path.join(self.path_dir_temp, 'order.docx'), cont_dict['chk_state'][2], 'order'),
			(os.path.join(self.path_dir_temp, 'act_tmc.docx'), cont_dict['chk_state'][3], 'act_tmc')
		)

		for template in self.template:
			self.print_to_file(cont_dict, *template)

	def print_to_file(self, dict_text: dict, template: str, pref: int = 0, pref_name: str = ''):
		if pref:
			document = DocxTemplate(template)

			rorder = RichText()
			rdata = RichText()
			rname = RichText()
			rbrand = RichText()
			rnum = RichText()
			radr = RichText()
			rdriv = RichText()
			rphone = RichText()
			rmphone = RichText()
			rcurdata = RichText()

			radr.add(dict_text['address'], size=28)
			rdriv.add(dict_text['driver'], size=28)
			rphone.add(dict_text['phone'], size=28)
			rmphone.add(dict_text['mphone'], size=28)

			if pref_name == 'act_tmc':
				rorder.add('{}-{}'.format(dict_text['order_number'], dict_text['prefix']), size=40, bold=True, underline=True)
				rdata.add(dict_text['curdata'], size=36, bold=True)
				rname.add(dict_text['name'], size=36, bold=True)
				rbrand.add(dict_text['brand'], size=32, bold=True)
				rnum.add(dict_text['car_number'], size=32, bold=True)
				rcurdata.add(dict_text['curdata'], size=36, bold=True, underline=True)
			else:
				rorder.add(dict_text['order_number'], size=28, bold=True)
				rdata.add(dict_text['curdata'], size=28)
				rname.add(dict_text['name'], size=28)
				rbrand.add(dict_text['brand'], size=28)
				rnum.add(dict_text['car_number'], size=28)
				rcurdata.add(dict_text['curdata'], size=28)

			new_dict = {
				'order_number': rorder,
				'crdata': rdata,
				'name': rname,
				'brand': rbrand,
				'car_number': rnum,
				'address': radr,
				'driver': rdriv,
				'phone': rphone,
				'mphone': rmphone,
				'curdata': rcurdata
			}

			document.render(new_dict)

			path = os.path.join(self.path_dir_order_file, dict_text['path_file_dir'])
			self.exists_file(path)

			path_sep = "{path}{sep}".format(path=path, sep=os.sep)
			path_file = "{path}{name}_{pref}".format(
				path=path_sep,
				name=dict_text['file_name'],
				pref=pref_name)

			document.save(path_file + '.docx')
			
			upd = CreateDB()
			upd.update_order_path(int(dict_text['order_id']), path)

			if sys.platform == 'win32':
				self.print_to_print(path_file + '.docx')
			# if sys.platform == 'linux':
			# 	convert_to(path_sep, path_file + '.docx')
			# 	self.print_to_print(path_file + '.pdf')

	@classmethod
	def print_to_print(cls, path):
		if sys.platform == 'win32':
			ShellExecute(
				0,
				'printto',
				path,
				'/d:"%s"' % GetDefaultPrinter(),
				'.',
				0
			)
			# os.startfile(path, "print")
		# if sys.platform == 'linux':
		# 	os.system('lpr ' + path)

	@classmethod
	def exists_file(cls, path):
		if not os.path.exists(path):
			os.makedirs(path)


# def convert_to(folder, source, timeout=None):
# 	args = [libreoffice_exec(), '--headless', '--convert-to', 'pdf', '--outdir', folder, source]
#
# 	process = subprocess.run(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=timeout)
# 	filename = re.search('-> (.*?) using filter', process.stdout.decode())
#
# 	if filename is None:
# 		raise LibreOfficeError(process.stdout.decode())
# 	else:
# 		return filename.group(1)
#
#
# def libreoffice_exec():
# 	if sys.platform == 'darwin':
# 		return '/Applications/LibreOffice.app/Contents/MacOS/soffice'
# 	return 'libreoffice'
#
#
# class LibreOfficeError(Exception):
# 	def __init__(self, output):
# 		self.output = output


if __name__ == '__main__':
	pass
