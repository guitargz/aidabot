from transformers import pipeline, set_seed
import random
import time
import gc

def generate_caption(seed):
    generator = pipeline('text-generation', model='gpt2')
    set_seed(seed)
    caption = generator("My today Instagram beauty blogger post is: ", max_length=100, num_return_sequences=1)

    #free memory
    del generator
    gc.collect()

    caption = u''.join(caption[0]['generated_text'][42:])
    for sep in '.!?':
        caption = u''.join(caption).rsplit(sep, 1)
        if len(caption) > 1:
            return (str(caption[0])+sep)
    return caption

def main():
    file = "results/Demo_today.txt"
    while True:
        files = open(file, 'wb')
        caption = generate_caption(random.randint(1, 999999999))
        caption = u''.join(caption).encode('utf-8', 'ignore')
        files.write(caption)
        files.close()
        time.sleep(21600)

if __name__ == "__main__":
    main()
