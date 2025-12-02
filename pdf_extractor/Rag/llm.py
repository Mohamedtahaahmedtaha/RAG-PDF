#from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline

#def load_llm():
 #   model_name = "Qwen/Qwen2.5-0.5B-Instruct"  

  #  tokenizer = AutoTokenizer.from_pretrained(model_name, trust_remote_code=True)
   # model = AutoModelForCausalLM.from_pretrained(model_name, torch_dtype="auto")

   # return pipeline(
    #    task="text-generation",
     #   model=model,
      #  tokenizer=tokenizer,
       # max_new_tokens=512,
       # temperature=0.2,
        #top_p=0.9,
        #device=-1  # -1 → CPU, أو 0 → GPU
    #)