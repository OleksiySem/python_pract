def process_string(letters):
    vowel = 'aeiouAEIOU'
    vowel_list = []
    consonant_list = []

    for ch in letters:
        if ch.isalpha():
            if ch in vowel:
                vowel_list.append(ch)
            else:
                consonant_list.append(ch)

    vowel_str = ''
    for v in vowel_list:
        vowel_str += v

    consonant_str = ''
    for c in consonant_list:
        consonant_str += c

    consonant_number = len(consonant_list)

    return (vowel_str, consonant_number, consonant_str)

input_str = input()
result = process_string(input_str)
print(result)
