from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

tokenizer = AutoTokenizer.from_pretrained("google/flan-t5-small")
model = AutoModelForSeq2SeqLM.from_pretrained("google/flan-t5-small")

tokenizer.save_pretrained("/app/model/flan_t5_small_tokenizer")
model.save_pretrained("/app/model/flan_t5_small_model")
