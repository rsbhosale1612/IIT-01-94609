sentence = input("Enter the sentence: ")

charnum = len(sentence)


words = sentence.split()
wordnum = len(words)


vowels = "aeiouAEIOU"
vowelnum = 0

for ch in sentence:
    if ch in vowels:
        vowelnum += 1


print("Number of characters:", charnum)
print("Number of words:", wordnum)
print("Number of vowels:", vowelnum)
