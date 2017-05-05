import requests


def get_sentiment(string_list):
    sentiment = 0
    for string in string_list:
        print(string)
        r = requests.post('http://text-processing.com/api/sentiment/', data={'text': string})
        json_response = r.json()
        label = json_response['label']
        # string_dict['label'] = label
        if label == 'pos':
            sentiment += 2
        elif label == 'neg':
            sentiment -= 2
        else:
            neutral += 1

        d = {'positive': positive, 'negative': negative, 'neutral': neutral}
    return d


