import random
import base64
import hashlib
import json
def addWord(id, word):
    
    # try:
    #     # uuser = user.objects.get(uid = id)
    #     # bookpath = uuser.dict 
    #     bookpath = "C:\\Users\\Administrator\\Desktop\\voca.json"

    #     with open(bookpath, 'w') as f:
    #         print("?")
    #         allwords = dict(json.load(f))
    #         print(allwords+"ss")

    #         if word in allwords.keys():
    #             allwords[word] = allwords[word] + 1
    #         else:
    #             allwords[word] = 0

    #         f.write(json.dumps(allwords))

    # except:
    #     print("添加单词出错...")
    #     return False
    allwords = {}
    bookpath = "C:\\Users\\Administrator\\Desktop\\voca.json"
    
    with open(bookpath, 'r') as f:
        allwords = dict(json.load(f))

    with open(bookpath, 'w') as f:
        if word in allwords.keys():
            allwords[word] = allwords[word] + 1
        else:
            allwords[word] = 0

        f.write(json.dumps(allwords))

    return True

addWord("haha","word")