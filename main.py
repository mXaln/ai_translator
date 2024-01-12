from functools import partial
from threading import Thread
from kivy.core.window import Window
from kivy.app import App
from kivy.clock import mainthread
from kivy.properties import ObjectProperty, StringProperty, NumericProperty, ListProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.widget import Widget
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, pipeline


class BlockingOverlay(BoxLayout):
    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos) and self.opacity > 0:
            return True
        return super(BlockingOverlay, self).on_touch_down(touch)


class MainView(Widget):
    languages = {
        "Acehnese (Arabic script)": "ace_Arab",
        "Acehnese (Latin script)": "ace_Latn",
        "Mesopotamian Arabic": "acm_Arab",
        "Ta’izzi-Adeni Arabic": "acq_Arab",
        "Tunisian Arabic": "aeb_Arab",
        "Afrikaans": "afr_Latn",
        "South Levantine Arabic": "ajp_Arab",
        "Akan": "aka_Latn",
        "Amharic": "amh_Ethi",
        "North Levantine Arabic": "apc_Arab",
        "Modern Standard Arabic": "arb_Arab",
        "Modern Standard Arabic (Romanized)": "arb_Latn",
        "Najdi Arabic": "ars_Arab",
        "Moroccan Arabic": "ary_Arab",
        "Egyptian Arabic": "arz_Arab",
        "Assamese": "asm_Beng",
        "Asturian": "ast_Latn",
        "Awadhi": "awa_Deva",
        "Central Aymara": "ayr_Latn",
        "South Azerbaijani": "azb_Arab",
        "North Azerbaijani": "azj_Latn",
        "Bashkir": "bak_Cyrl",
        "Bambara": "bam_Latn",
        "Balinese": "ban_Latn",
        "Belarusian": "bel_Cyrl",
        "Bemba": "bem_Latn",
        "Bengali": "ben_Beng",
        "Bhojpuri": "bho_Deva",
        "Banjar (Arabic script)": "bjn_Arab",
        "Banjar (Latin script)": "bjn_Latn",
        "Standard Tibetan": "bod_Tibt",
        "Bosnian": "bos_Latn",
        "Buginese": "bug_Latn",
        "Bulgarian": "bul_Cyrl",
        "Catalan": "cat_Latn",
        "Cebuano": "ceb_Latn",
        "Czech": "ces_Latn",
        "Chokwe": "cjk_Latn",
        "Central Kurdish": "ckb_Arab",
        "Crimean Tatar": "crh_Latn",
        "Welsh": "cym_Latn",
        "Danish": "dan_Latn",
        "German": "deu_Latn",
        "Southwestern Dinka": "dik_Latn",
        "Dyula": "dyu_Latn",
        "Dzongkha": "dzo_Tibt",
        "Greek": "ell_Grek",
        "English": "eng_Latn",
        "Esperanto": "epo_Latn",
        "Estonian": "est_Latn",
        "Basque": "eus_Latn",
        "Ewe": "ewe_Latn",
        "Faroese": "fao_Latn",
        "Fijian": "fij_Latn",
        "Finnish": "fin_Latn",
        "Fon": "fon_Latn",
        "French": "fra_Latn",
        "Friulian": "fur_Latn",
        "Nigerian Fulfulde": "fuv_Latn",
        "Scottish Gaelic": "gla_Latn",
        "Irish": "gle_Latn",
        "Galician": "glg_Latn",
        "Guarani": "grn_Latn",
        "Gujarati": "guj_Gujr",
        "Haitian Creole": "hat_Latn",
        "Hausa": "hau_Latn",
        "Hebrew": "heb_Hebr",
        "Hindi": "hin_Deva",
        "Chhattisgarhi": "hne_Deva",
        "Croatian": "hrv_Latn",
        "Hungarian": "hun_Latn",
        "Armenian": "hye_Armn",
        "Igbo": "ibo_Latn",
        "Ilocano": "ilo_Latn",
        "Indonesian": "ind_Latn",
        "Icelandic": "isl_Latn",
        "Italian": "ita_Latn",
        "Javanese": "jav_Latn",
        "Japanese": "jpn_Jpan",
        "Kabyle": "kab_Latn",
        "Jingpho": "kac_Latn",
        "Kamba": "kam_Latn",
        "Kannada": "kan_Knda",
        "Kashmiri (Arabic script)": "kas_Arab",
        "Kashmiri (Devanagari script)": "kas_Deva",
        "Georgian": "kat_Geor",
        "Central Kanuri (Arabic script)": "knc_Arab",
        "Central Kanuri (Latin script)": "knc_Latn",
        "Kazakh": "kaz_Cyrl",
        "Kabiyè": "kbp_Latn",
        "Kabuverdianu": "kea_Latn",
        "Khmer": "khm_Khmr",
        "Kikuyu": "kik_Latn",
        "Kinyarwanda": "kin_Latn",
        "Kyrgyz": "kir_Cyrl",
        "Kimbundu": "kmb_Latn",
        "Northern Kurdish": "kmr_Latn",
        "Kikongo": "kon_Latn",
        "Korean": "kor_Hang",
        "Lao": "lao_Laoo",
        "Ligurian": "lij_Latn",
        "Limburgish": "lim_Latn",
        "Lingala": "lin_Latn",
        "Lithuanian": "lit_Latn",
        "Lombard": "lmo_Latn",
        "Latgalian": "ltg_Latn",
        "Luxembourgish": "ltz_Latn",
        "Luba-Kasai": "lua_Latn",
        "Ganda": "lug_Latn",
        "Luo": "luo_Latn",
        "Mizo": "lus_Latn",
        "Standard Latvian": "lvs_Latn",
        "Magahi": "mag_Deva",
        "Maithili": "mai_Deva",
        "Malayalam": "mal_Mlym",
        "Marathi": "mar_Deva",
        "Minangkabau (Arabic script)": "min_Arab",
        "Minangkabau (Latin script)": "min_Latn",
        "Macedonian": "mkd_Cyrl",
        "Plateau Malagasy": "plt_Latn",
        "Maltese": "mlt_Latn",
        "Meitei (Bengali script)": "mni_Beng",
        "Halh Mongolian": "khk_Cyrl",
        "Mossi": "mos_Latn",
        "Maori": "mri_Latn",
        "Burmese": "mya_Mymr",
        "Dutch": "nld_Latn",
        "Norwegian Nynorsk": "nno_Latn",
        "Norwegian Bokmål": "nob_Latn",
        "Nepali": "npi_Deva",
        "Northern Sotho": "nso_Latn",
        "Nuer": "nus_Latn",
        "Nyanja": "nya_Latn",
        "Occitan": "oci_Latn",
        "West Central Oromo": "gaz_Latn",
        "Odia": "ory_Orya",
        "Pangasinan": "pag_Latn",
        "Eastern Panjabi": "pan_Guru",
        "Papiamento": "pap_Latn",
        "Western Persian": "pes_Arab",
        "Polish": "pol_Latn",
        "Portuguese": "por_Latn",
        "Dari": "prs_Arab",
        "Southern Pashto": "pbt_Arab",
        "Ayacucho Quechua": "quy_Latn",
        "Romanian": "ron_Latn",
        "Rundi": "run_Latn",
        "Russian": "rus_Cyrl",
        "Sango": "sag_Latn",
        "Sanskrit": "san_Deva",
        "Santali": "sat_Olck",
        "Sicilian": "scn_Latn",
        "Shan": "shn_Mymr",
        "Sinhala": "sin_Sinh",
        "Slovak": "slk_Latn",
        "Slovenian": "slv_Latn",
        "Samoan": "smo_Latn",
        "Shona": "sna_Latn",
        "Sindhi": "snd_Arab",
        "Somali": "som_Latn",
        "Southern Sotho": "sot_Latn",
        "Spanish": "spa_Latn",
        "Tosk Albanian": "als_Latn",
        "Sardinian": "srd_Latn",
        "Serbian": "srp_Cyrl",
        "Swati": "ssw_Latn",
        "Sundanese": "sun_Latn",
        "Swedish": "swe_Latn",
        "Swahili": "swh_Latn",
        "Silesian": "szl_Latn",
        "Tamil": "tam_Taml",
        "Tatar": "tat_Cyrl",
        "Telugu": "tel_Telu",
        "Tajik": "tgk_Cyrl",
        "Tagalog": "tgl_Latn",
        "Thai": "tha_Thai",
        "Tigrinya": "tir_Ethi",
        "Tamasheq (Latin script)": "taq_Latn",
        "Tamasheq (Tifinagh script)": "taq_Tfng",
        "Tok Pisin": "tpi_Latn",
        "Tswana": "tsn_Latn",
        "Tsonga": "tso_Latn",
        "Turkmen": "tuk_Latn",
        "Tumbuka": "tum_Latn",
        "Turkish": "tur_Latn",
        "Twi": "twi_Latn",
        "Central Atlas Tamazight": "tzm_Tfng",
        "Uyghur": "uig_Arab",
        "Ukrainian": "ukr_Cyrl",
        "Umbundu": "umb_Latn",
        "Urdu": "urd_Arab",
        "Northern Uzbek": "uzn_Latn",
        "Venetian": "vec_Latn",
        "Vietnamese": "vie_Latn",
        "Waray": "war_Latn",
        "Wolof": "wol_Latn",
        "Xhosa": "xho_Latn",
        "Eastern Yiddish": "ydd_Hebr",
        "Yoruba": "yor_Latn",
        "Yue Chinese": "yue_Hant",
        "Chinese (Simplified)": "zho_Hans",
        "Chinese (Traditional)": "zho_Hant",
        "Standard Malay": "zsm_Latn",
        "Zulu": "zul_Latn"
    }
    sorted_languages = {}

    model = None
    tokenizer = None

    langs = ListProperty()
    src_selected = StringProperty()
    target_selected = StringProperty()

    src_text = StringProperty()
    target_text = StringProperty()

    overlay_opacity = NumericProperty(0)
    overlay_text = StringProperty()

    src_dropdown = ObjectProperty(None)
    target_dropdown = ObjectProperty(None)
    last_found_lang = StringProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.keyboard = Window.request_keyboard(self.keyboard_closed, self)
        self.keyboard.bind(on_key_up=self.on_key_up)

        self.sorted_languages = dict(sorted(self.languages.items()))

        self.langs = tuple(self.sorted_languages.keys())
        self.src_selected = "Select Source Language"
        self.target_selected = "Select Target Language"

    def keyboard_closed(self):
        self.keyboard.unbind(on_key_up=self.on_key_up)
        self.keyboard = None

    def on_key_up(self, keyboard, keycode):
        code = keycode[1]

        if self.src_dropdown.is_open:
            self.find_lang(self.src_dropdown, code)
        elif self.target_dropdown.is_open:
            self.find_lang(self.target_dropdown, code)

        return True

    def find_lang(self, widget, key):
        keys = list(self.sorted_languages.keys())
        found = [k for k in keys if k.lower().startswith(key)]

        if found:
            for lang in found:
                curr_index = found.index(lang)
                last_index = found.index(self.last_found_lang) if self.last_found_lang in found else -1

                if lang != self.last_found_lang and curr_index > last_index:
                    self.last_found_lang = lang
                    break

                if last_index == len(found) - 1:
                    self.last_found_lang = ""
                    break

            if self.last_found_lang:
                widget.text = self.last_found_lang

    def load_model(self):
        if self.model is None:
            self.model = AutoModelForSeq2SeqLM.from_pretrained("facebook/nllb-200-distilled-600M")
        if self.tokenizer is None:
            self.tokenizer = AutoTokenizer.from_pretrained("facebook/nllb-200-distilled-600M")

    def translate(self, *args):
        try:
            src_lang = self.languages[self.src_selected]
            target_lang = self.languages[self.target_selected]
            src_text = self.src_text

            if src_text != "":
                self.show_progress()

                Thread(target=partial(self.do_translate, src_lang, target_lang, src_text)).start()
            else:
                self.show_popup("Error", "Enter text to translate.")

        except Exception as error:
            print(error)
            self.show_popup("Error", str(error))

    def do_translate(self, src_lang, target_lang, src_text):
        App.get_running_app().root.update_progress("Loading model...")
        self.load_model()

        App.get_running_app().root.update_progress("Translating...")
        translator = pipeline("translation",
                              model=self.model, tokenizer=self.tokenizer,
                              src_lang=src_lang, tgt_lang=target_lang,
                              max_length=4000)
        payload = translator(src_text)
        print(payload)
        result = payload[0]["translation_text"]

        App.get_running_app().root.update_target(result)
        App.get_running_app().root.hide_progress()

    @mainthread
    def update_target(self, result):
        self.target_text = result

    @mainthread
    def show_popup(self, title, message):
        layout = BoxLayout(orientation="vertical")

        label = Label(text=message)
        close = Button(text="OK",
                       size_hint=(None, None), width=100, height=40,
                       pos_hint={'center_x': 0.5, 'center_y': 0.5})

        layout.add_widget(label)
        layout.add_widget(close)

        popup = Popup(title=title, content=layout, size_hint=(None, None), width=600, height=400)
        popup.open()

        close.bind(on_release=popup.dismiss)

    @mainthread
    def show_progress(self):
        self.overlay_opacity = 0.9

    @mainthread
    def hide_progress(self):
        self.overlay_opacity = 0

    @mainthread
    def update_progress(self, message):
        self.overlay_text = message


class AiTranslator(App):
    def build(self):
        return MainView()


def main():
    AiTranslator().run()


if __name__ == "__main__":
    main()
