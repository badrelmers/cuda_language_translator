import os
import platform
from cudatext import *
from pathlib import Path
import sys
import urllib.request, urllib.parse, json
import asyncio
from cudax_lib import get_translation
_ = get_translation(__file__)

sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'libs'))

from googletrans import Translator, constants
import pyperclip

class Command:
    def __init__(self):
        self.conf_file = Path(app_path(APP_DIR_SETTINGS)) / 'cuda_language_translator.json'
        self.translator = Translator()
        self.languages = constants.LANGUAGES
        self.target_lang = 'en'

    def translate(self, text, target_lang):
        if text:
            return "".join(p[0] for p in json.loads(urllib.request.urlopen(urllib.request.Request("https://translate.googleapis.com/translate_a/single?client=gtx&sl=auto&tl="+target_lang+"&dt=t&q="+urllib.parse.quote(text),headers={"User-Agent":"Mozilla/5.0"})).read())[0])

        return None

    def show_language_menu(self):
        langs = '\n' . join([f"{code}: {name}" for code, name in self.languages.items()])
        res = dlg_menu(DMENU_LIST, langs, 0, _('Select target language'))
        if res is not None:
            selected_code = list(self.languages.keys())[res]
            self.target_lang = selected_code
            return selected_code

        return None

    def translate_with_selection(self):
        selected_lang = self.show_language_menu()
        if selected_lang:
            txt = ed.get_text_sel()
            if len(txt) > 0:
                return self.translate(txt, selected_lang)

        return None

    def res2tab(self):
        translated = self.translate_with_selection()
        if translated:
            file_open('')
            ed.set_text_all(translated)
            self.actc(translated)

    def res2msgbox(self):
        translated = self.translate_with_selection()
        if translated:
            msg_box(translated, MB_OK + MB_ICONINFO)
            self.actc(translated)

    def res2clipboard(self):
        translated = self.translate_with_selection()
        if translated:
            pyperclip.copy(translated)
            msg_status('Language Translator: ' + _('translated text copied to clipboard.'))

    def res2statusbar(self):
        translated = self.translate_with_selection()
        if translated:
            msg_status('Language Translator: ' + translated)
            self.actc(translated)

    def config(self):
        if self.conf_file.exists() == False:
            with self.conf_file.open(mode='w', encoding='utf-8') as f:
                json.dump({'automatic copy to clipboard': 0}, f, indent=2)
        file_open(str(self.conf_file))

    def check_option(self, option):
        data = {}
        if self.conf_file.exists():
            with self.conf_file.open(encoding='utf-8') as f:
                data = json.load(f)
        for param, val in data.items():
            if (param == option and val == 1):
                return True

        return False

    def actc(self, translated):
        if self.check_option('automatic copy to clipboard'):
            pyperclip.copy(translated)
            msg_status('Language Translator: ' + _('translated text copied to clipboard (option: automatic copy to clipboard).'))