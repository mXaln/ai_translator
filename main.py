from PyQt5 import QtWidgets, QtCore

from components.overlay import OverlayWidget
from components.workspace import WorkspaceWidget
from models.languages import LanguagesModel
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, pipeline


class TranslatorSignals(QtCore.QObject):
    error = QtCore.pyqtSignal(str)
    result = QtCore.pyqtSignal(object)


class Translator(QtCore.QRunnable):
    def __init__(self, fn, *args, **kwargs):
        super(Translator, self).__init__()

        self.fn = fn
        self.args = args
        self.kwargs = kwargs
        self.signals = TranslatorSignals()

    @QtCore.pyqtSlot()
    def run(self):
        try:
            result = self.fn(*self.args, **self.kwargs)
            self.signals.result.emit(result)
        except Exception as e:
            self.signals.error.emit(str(e))


class MainWindow(QtWidgets.QMainWindow):
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

    overlay = None
    lang_model = None

    target_text = ""

    model = None
    tokenizer = None

    def __init__(self):
        super().__init__()

        self.threadpool = QtCore.QThreadPool()

        self.languages = dict(sorted(self.languages.items()))
        self.lang_model = LanguagesModel(self.languages)

        self.setWindowTitle("AiTranslator")
        self.setMinimumSize(QtCore.QSize(500, 400))

        layout = QtWidgets.QStackedLayout()
        layout.setStackingMode(QtWidgets.QStackedLayout.StackingMode.StackAll)

        self.workspace = WorkspaceWidget(self.lang_model)
        self.workspace.translate.connect(self.on_translate)
        layout.addWidget(self.workspace)

        self.overlay = OverlayWidget("...")
        layout.addWidget(self.overlay)

        widget = QtWidgets.QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

    def show_overlay(self):
        self.overlay.setVisible(True)

    def hide_overlay(self):
        self.overlay.setVisible(False)

    def update_overlay(self, message):
        self.overlay.setText(message)

    def on_translate(self):
        self.show_overlay()
        self.start_model_loader()

    def start_translator(self):
        src_lang = self.get_source_lang()
        target_lang = self.get_target_lang()
        src_text = self.get_source_text().strip()

        try:
            if src_lang not in self.languages:
                raise Exception("Select source language.")

            if target_lang not in self.languages:
                raise Exception("Select target language.")

            if src_text == "":
                raise Exception("Source text cannot be empty.")

            src_code = self.languages[src_lang]
            target_code = self.languages[target_lang]

            translator = Translator(self.do_translate, src_code, target_code, src_text)
            translator.signals.result.connect(self.on_translate_done)
            translator.signals.error.connect(self.on_translator_error)

            self.threadpool.start(translator)
        except Exception as e:
            self.on_translator_error(str(e))

    def do_translate(self, src_lang, target_lang, src_text):
        translator = pipeline("translation",
                              model=self.model, tokenizer=self.tokenizer,
                              src_lang=src_lang, tgt_lang=target_lang,
                              max_length=1000000)

        target_text = ""
        for line in src_text.splitlines():
            text = line.strip()
            if text:
                payload = translator(text)
                target_text += payload[0]["translation_text"] + "\n"
            else:
                target_text += "\n\n"

        return target_text

    def start_model_loader(self):
        self.update_overlay("Loading models...")

        if self.model is None and self.tokenizer is None:
            model_loader = Translator(self.load_models)
            model_loader.signals.result.connect(self.on_models_loaded)
            model_loader.signals.error.connect(self.on_translator_error)

            self.threadpool.start(model_loader)
        else:
            self.on_models_loaded((self.model, self.tokenizer))

    def load_models(self):
        model = AutoModelForSeq2SeqLM.from_pretrained("facebook/nllb-200-distilled-600M")
        tokenizer = AutoTokenizer.from_pretrained("facebook/nllb-200-distilled-600M")

        return model, tokenizer

    def on_models_loaded(self, models):
        self.model, self.tokenizer = models

        self.update_overlay("Translating...")
        self.start_translator()

    def on_translate_done(self, text):
        self.set_target_text(text)
        self.hide_overlay()

    def on_translator_error(self, error):
        self.hide_overlay()

        QtWidgets.QMessageBox.critical(self, "An error occurred", error)

    def set_source_text(self, text):
        self.workspace.set_source_text(text)

    def get_source_text(self):
        return self.workspace.get_source_text()

    def get_source_lang(self):
        return self.workspace.get_source_lang()

    def set_target_text(self, text):
        self.workspace.set_target_text(text)

    def get_target_text(self):
        return self.workspace.get_target_text()

    def get_target_lang(self):
        return self.workspace.get_target_lang()


def main():
    app = QtWidgets.QApplication([])

    window = MainWindow()
    window.show()

    app.exec()


if __name__ == "__main__":
    main()
