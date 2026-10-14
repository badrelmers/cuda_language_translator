import os
import platform
from cudatext import *
from pathlib import Path
import sys
import urllib.request, urllib.parse, json
from cudax_lib import get_translation
_ = get_translation(__file__)

sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'libs'))
import pyperclip

class Command:
    def __init__(self):
        self.conf_file = Path(app_path(APP_DIR_SETTINGS)) / 'cuda_language_translator.json'
        self.languages = {'abk':'abkhaz','ace':'acehnese','ach':'acholi','aar':'afar','af':'afrikaans','sq':'albanian','alz':'alur','am':'amharic','ar':'arabic','hy':'armenian','as':'assamese','ava':'avar','awa':'awadhi','ay':'aymara','az':'azerbaijani','ban':'balinese','bal':'baluchi','bm':'bambara','bci':'baoulé','bak':'bashkir','eu':'basque','btx':'batak karo','bts':'batak simalungun','bbc':'batak toba','be':'belarusian','bem':'bemba','bn':'bengali','bew':'betawi','bho':'bhojpuri','bik':'bikol','bs':'bosnian','bre':'breton','bg':'bulgarian','bua':'buryat','yue':'cantonese','ca':'catalan','ceb':'cebuano','cha':'chamorro','che':'chechen','zh':'chinese','zh-cn':'chinese (simplified)','zh-tw':'chinese (traditional)','chk':'chuukese','chv':'chuvash','co':'corsican','crh':'crimean tatar','hr':'croatian','cs':'czech','da':'danish','fa-af':'dari','dv':'dhivehi','din':'dinka','doi':'dogri','dom':'dombe','nl':'dutch','dyu':'dyula','dzo':'dzongkha','en':'english','eo':'esperanto','et':'estonian','fao':'faroese','fij':'fijian','fil':'filipino (tagalog)','fi':'finnish','fon':'fon','fr':'french','fy':'frisian','fur':'friulian','ful':'fulani','gaa':'ga','gl':'galician','ka':'georgian','de':'german','el':'greek','gn':'guarani','gu':'gujarati','ht':'haitian creole','cnh':'hakha chin','ha':'hausa','haw':'hawaiian','he':'hebrew','iw':'hebrew','hil':'hiligaynon','hi':'hindi','hmn':'hmong','hu':'hungarian','hrx':'hunsrik','iba':'iban','is':'icelandic','ig':'igbo','ilo':'ilocano','id':'indonesian','ga':'irish','it':'italian','jam':'jamaican patois','ja':'japanese','jv':'javanese','jw':'javanese','kac':'jingpo','kal':'kalaallisut','kn':'kannada','kau':'kanuri','pam':'kapampangan','kk':'kazakh','kha':'khasi','km':'khmer','cgg':'kiga','kik':'kikongo','rw':'kinyarwanda','ktu':'kituba','trp':'kokborok','kom':'komi','gom':'konkani','ko':'korean','kri':'krio','ku':'kurdish','ckb':'kurdish (sorani)','ky':'kyrgyz','lo':'lao','ltg':'latgalian','la':'latin','lv':'latvian','lij':'ligurian','lim':'limburgish','ln':'lingala','lt':'lithuanian','lmo':'lombard','lg':'luganda','luo':'luo','lb':'luxembourgish','mk':'macedonian','mad':'madurese','mai':'maithili','mak':'makassar','mg':'malagasy','ms':'malay','ms-arab':'malay (jawi)','ml':'malayalam','mt':'maltese','mam':'mam','glv':'manx','mi':'maori','mr':'marathi','mah':'marshallese','mwr':'marwadi','mfe':'mauritian creole','mhr':'meadow mari','mni-mtei':'meiteilon (manipuri)','min':'minang','lus':'mizo','mn':'mongolian','my':'myanmar (burmese)','nhe':'nahuatl (eastern huasteca)','ndc-zw':'ndau','nde':'ndebele (south)','new':'nepalbhasa (newari)','ne':'nepali','no':'norwegian','nus':'nuer','ny':'nyanja (chichewa)','oci':'occitan','or':'odia (oriya)','om':'oromo','oss':'ossetian','pag':'pangasinan','pap':'papiamento','ps':'pashto','fa':'persian','pl':'polish','por':'portuguese (portugal)','pt':'portuguese (portugal,brazil)','pa':'punjabi','pa-arab':'punjabi (shahmukhi)','kek':"q'eqchi'",'qu':'quechua','rom':'romani','ro':'romanian','run':'rundi','ru':'russian','sme':'sami (north)','sm':'samoan','sag':'sango','sa':'sanskrit','sat':'santali','gd':'scots gaelic','nso':'sepedi','sr':'serbian','st':'sesotho','crs':'seychellois creole','shn':'shan','sn':'shona','scn':'sicilian','szl':'silesian','sd':'sindhi','si':'sinhala (sinhalese)','sk':'slovak','sl':'slovenian','so':'somali','es':'spanish','su':'sundanese','sus':'susu','sw':'swahili','ssw':'swati','sv':'swedish','tl':'tagalog (filipino)','tah':'tahitian','tg':'tajik','ber-atn':'tamazight','ber':'tamazight (tifinagh)','ta':'tamil','tt':'tatar','te':'telugu','tet':'tetum','th':'thai','bod':'tibetan','ti':'tigrinya','tiv':'tiv','tpi':'tok pisin','ton':'tongan','ts':'tsonga','tsn':'tswana','tcy':'tulu','tum':'tumbuka','tr':'turkish','tk':'turkmen','tuk':'tuvan','ak':'twi (akan)','udm':'udmurt','uk':'ukrainian','ur':'urdu','ug':'uyghur','uz':'uzbek','ven':'venda','vec':'venetian','vi':'vietnamese','war':'waray','cy':'welsh','wol':'wolof','xh':'xhosa','sah':'yakut','yi':'yiddish','yo':'yoruba','yua':'yucatec maya','zap':'zapotec','zu':'zulu'}

    def translate(self, text, target_lang):
        if text:
            return "".join(p[0] for p in json.loads(urllib.request.urlopen(urllib.request.Request("https://translate.googleapis.com/translate_a/single?client=gtx&sl=auto&tl="+target_lang+"&dt=t&q="+urllib.parse.quote(text),headers={"User-Agent":"Mozilla/5.0"})).read())[0])

        return None

    def show_language_menu(self):
        langs = '\n' . join([f"{code}: {name}" for code, name in self.languages.items()])
        res = dlg_menu(DMENU_LIST, langs, 0, _('Select target language'))
        if res is not None:
            return list(self.languages.keys())[res]

        return 'en'

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