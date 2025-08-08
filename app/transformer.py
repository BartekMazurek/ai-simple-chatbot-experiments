from transformers import T5Tokenizer, T5ForConditionalGeneration

TOKENIZER_PATH = "/model/flan_t5_small_tokenizer"
LLM_PATH = "/model/flan_t5_small_model"

tokenizer = T5Tokenizer.from_pretrained(TOKENIZER_PATH)
llm = T5ForConditionalGeneration.from_pretrained(LLM_PATH)
