import tkinter as tk
from tkinter import ttk

from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, pipeline


class App(tk.Tk):
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

    src_lang = None
    src_input = None
    target_lang = None
    target_input = None

    model = None
    tokenizer = None

    sorted_languages = {}

    def __init__(self):
        super().__init__()

        self.sorted_languages = dict(sorted(self.languages.items()))

        self.init_model()
        self.build_ui()

    def init_model(self):
        self.model = AutoModelForSeq2SeqLM.from_pretrained("facebook/nllb-200-distilled-600M")
        self.tokenizer = AutoTokenizer.from_pretrained("facebook/nllb-200-distilled-600M")

    def build_ui(self):
        self.title("Translator")
        self.geometry("700x400")
        self.minsize(700, 400)

        # create all the main containers
        top_pane = tk.Frame(self, pady=10)
        center_pane = tk.Frame(self, padx=10, pady=10)
        left_pane = tk.Frame(center_pane, padx=5, pady=5)
        right_pane = tk.Frame(center_pane, padx=5, pady=5)
        bottom_pane = tk.Frame(self, pady=10)

        # layout all the main containers
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        center_pane.grid_rowconfigure(0, weight=1)
        center_pane.grid_columnconfigure(0, weight=1)
        center_pane.grid_columnconfigure(1, weight=1)

        left_pane.grid_rowconfigure(1, weight=1)
        left_pane.grid_columnconfigure(0, weight=1)
        right_pane.grid_rowconfigure(1, weight=1)
        right_pane.grid_columnconfigure(0, weight=1)

        top_pane.grid(row=0)
        center_pane.grid(row=1, sticky="nsew")
        bottom_pane.grid(row=3)

        left_pane.grid(row=0, column=0, sticky="nsew")
        right_pane.grid(row=0, column=1, sticky="nsew")

        # Top pane widgets
        top_label = ttk.Label(top_pane, text="Translator")
        top_label.grid(row=0)

        # Center-Left pane widgets
        # Source language part
        self.src_lang = tk.StringVar(value="Select Source Language")
        src_list = ttk.Combobox(left_pane, textvariable=self.src_lang, state="readonly")
        src_list["values"] = list(self.sorted_languages.keys())
        src_list.grid(row=0, column=0, sticky="ew")

        self.src_input = tk.Text(left_pane)
        self.src_input.grid(row=1, column=0, sticky="nsew")

        # Center-Right pane widgets
        # Target language part
        self.target_lang = tk.StringVar(value="Select Target Language")
        target_list = ttk.Combobox(right_pane, textvariable=self.target_lang, state="readonly")
        target_list["values"] = list(self.sorted_languages.keys())
        target_list.grid(row=0, column=0, sticky="ew")

        self.target_input = tk.Text(right_pane)
        self.target_input.grid(row=1, column=0, sticky="nsew")

        # Bottom pane widgets
        button = ttk.Button(bottom_pane, text="Translate", width=10, command=self.translate)
        button.grid(row=0)

    def translate(self):
        try:
            src_lang = self.sorted_languages[self.src_lang.get()]
            target_lang = self.sorted_languages[self.target_lang.get()]
            src_text = self.src_input.get("1.0", tk.END).strip()

            if src_text != "":
                translator = pipeline("translation",
                                      model=self.model, tokenizer=self.tokenizer,
                                      src_lang=src_lang, tgt_lang=target_lang,
                                      max_length=4000)
                payload = translator(src_text)
                result = payload[0]["translation_text"]

                self.target_input.delete("1.0", tk.END)
                self.target_input.insert("1.0", result)

        except Exception as error:
            print(error)


if __name__ == "__main__":
    app = App()
    app.mainloop()
