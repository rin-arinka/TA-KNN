import pymongo
import urllib 
import numpy as np
from sklearn.neighbors import KNeighborsClassifier
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
count_vect = CountVectorizer()
client = pymongo.MongoClient("mongodb+srv://dimasdwi340:mypassword@cobaclusterku.osdwh.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
db = client['influcheck']
col = db['caption']
dataa = col.find()
class KNN_Classifier:    
    def profile_classifier(username):
        data_profile = KNN_Classifier.get_data_profile(username)
        data_train  = KNN_Classifier.train_profile_classifier()

        data_predict = [[data_profile['count_follower']], [data_profile['post_count']], [data_profile['verified']], [data_profile['professional']]]
        data_predict = np.array(data_predict)
        data_predict = data_predict.reshape(data_predict.shape[1], -1)
        X = data_train[0]
        y = data_train[1]
        X = np.array(X)
        X = X.reshape(X.shape[0], -1)
        neighbors = KNeighborsClassifier(n_neighbors=7)
        neighbors.fit(X, y)
        predict = neighbors.predict(data_predict)
        predict = predict.tolist()
        predict = predict[0]
        return predict

    def jenis_classifier(username):
        list_caption_profile = [KNN_Classifier.train_caption_classifier(username)]
        col = db['jenis']
        dataa = col.find()
        neigh = KNeighborsClassifier(n_neighbors=3)
        X = []
        y = []
        for data in dataa:
            X.append(eval(data['pola_caption']))
            y.append(data['label'])
        X = np.array(X)
        X = X.reshape(X.shape[0], -1)
        neigh.fit(X,y)
        list_caption_profile = np.array(list_caption_profile)
        list_caption_profile = list_caption_profile.reshape(list_caption_profile.shape[0], -1)
        predict = neigh.predict(list_caption_profile)
        predict = predict.tolist()
        predict = int(predict[0])
        print (list_caption_profile)
        if predict == 1:
            jenis = "Travel Blogger🚀"
        elif predict == 2:
            jenis = "Financial Advisor📊"
        else:
            jenis = "Belum Terdefinisikan😣"
        return jenis

    def get_profile(username):
        import requests
        import browser_cookie3
        cookiejar = browser_cookie3.opera(domain_name='instagram.com')
        try:
            data = requests.get(f'https://www.instagram.com/{username}/?__a=1&__d=dis', cookies = cookiejar).json()
            return data
        except :
            return ValueError

    def get_data_profile(username):
        
        data = KNN_Classifier.get_profile(username)  
        data_profile = data['graphql']['user']
        profile_pic = data_profile['profile_pic_url_hd']
        urllib.request.urlretrieve(f"{profile_pic}" , f"img/{username}.jpg")
        full_name = data_profile['full_name']
        follower = data_profile['edge_followed_by']['count']
        post_count = data_profile['edge_owner_to_timeline_media']['count']
        is_verified = data_profile['is_verified']
        is_profesional = data_profile['is_professional_account']
        bio = data_profile['biography']

        doc = dict(
            username = username,
            fullname = full_name,
            profile = profile_pic,
            count_follower = follower,
            post_count = post_count,
            verified = is_verified,
            professional = is_profesional,
            bio = bio
            )
        return doc
        

    def train_profile_classifier():
        col = db['influencer']
        data = col.find()
        X = []
        y = []
        for dataset in data:
            training = [[int(dataset['count_follower'])], [int(dataset['post_count'])], [int(dataset['verified'])], [int(dataset['professional'])]]
            X.append(training)
            y.append(dataset['label'])
        data = [X,y]
        return data

    def train_caption_classifier(username):
        from sklearn.naive_bayes import MultinomialNB
        col = db['caption']
        data_training = col.find()
        X = []
        y = []
        for data in data_training:
            X.append(data['caption'])
            y.append(data['label'])
        X_train = count_vect.fit_transform(X)
        tf_transformer = TfidfTransformer().fit(X_train)
        X_train = tf_transformer.transform(X_train)
        clf = MultinomialNB().fit(X_train, y)
        list_caption = KNN_Classifier.get_caption(username)
        X_predict = count_vect.transform(list_caption)
        X_predict = tf_transformer.transform(X_predict)
        predict = clf.predict(X_predict)
        predict = predict.tolist()
        int_predict = []
        for to_int in predict:
            integer = int(to_int)
            int_predict.append(integer)
        while len(int_predict)<24:
            int_predict.append(0)
        return int_predict

    def get_caption(username):
        data_caption = KNN_Classifier.get_profile(username)
        capt2doc = []
        data_profile = data_caption['graphql']['user']
        data_media_photo = data_profile['edge_owner_to_timeline_media']['edges']
        data_media_video = data_profile['edge_felix_video_timeline']['edges']
        
        for data_caption in range (len(data_media_photo)):
            caption = data_media_photo[data_caption]['node']['edge_media_to_caption']['edges']
            if not caption:
                capt2doc.append("")
            else:
                caption = caption[0]['node']['text']
                caption = KNN_Classifier.cleancapt(caption)
                capt2doc.append(caption)
        for data_caption in range (len(data_media_video)):
            caption = data_media_photo[data_caption]['node']['edge_media_to_caption']['edges']
            if not caption:
                capt2doc.append("")
            else:
                caption = caption[0]['node']['text']
                caption = KNN_Classifier.cleancapt(caption)
                capt2doc.append(caption)
        return capt2doc

    def stopwordindonesia():
        f = open("KNN/tala-stopwords-indonesia.txt", "r")
        stopword_listindonesia = []
        for line in f:
            stripped_line = line.strip()
            line_list = stripped_line.split()
            stopword_listindonesia.append(line_list[0])
        f.close()
        return stopword_listindonesia

    def stopwordenglish():
        e = open("KNN/stopword-english.txt", "r")
        stopword_listenglish = []
        for line in e:
            stripped_line = line.strip()
            line_list = stripped_line.split()
            stopword_listenglish.append(line_list[0])
        e.close()
        return stopword_listenglish

    def cleancapt(caption):
        from nltk.tokenize import word_tokenize
        from nltk.tokenize.treebank import TreebankWordDetokenizer
        import re
        from nltk.stem import SnowballStemmer
        snow = SnowballStemmer(language='english')
        from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
        factory = StemmerFactory()
        stemmer = factory.create_stemmer()
        detokenizer = TreebankWordDetokenizer()
        stopword_listindonesia = KNN_Classifier.stopwordindonesia()
        stopword_listenglish = KNN_Classifier.stopwordenglish()
        word = caption.lower()
        word = re.sub('[^\w\s]', "", str(word))
        word = re.sub('[0-9]+', "", str(word))
        word = re.sub("@\S+", "", str(word))
        word = re.sub("#", "", str(word))
        word = re.sub("\n", " ", str(word))
        word = re.sub("'", " ", str(word))
        tokenized = word_tokenize(word)
        indo_stopword = [word for word in tokenized if not word in stopword_listindonesia]
        english_stopword = [word for word in indo_stopword if not word in stopword_listenglish]
        word = [snow.stem(word) for word in english_stopword]
        word = detokenizer.detokenize(word)
        word = stemmer.stem(word)
        word = word.split() 
        word = " ".join(sorted(set(word), key=word.index))
        return word
        
    def get_img_post (username):
        data_profile = KNN_Classifier.get_profile(username)
        data_profile = data_profile['graphql']['user']
        data_media_photo = data_profile['edge_owner_to_timeline_media']['edges']
        list_shortcode = []
        list_like = []
        list_comment = []
        
        for data_caption in range (9):
            shortcode = data_media_photo[data_caption]['node']['shortcode']
            list_shortcode.append(shortcode)
            display_pic = data_media_photo[data_caption]['node']['display_url']
            urllib.request.urlretrieve(f"{display_pic}" , f"img_post/{username}{data_caption}.jpg")
            like = data_media_photo[data_caption]['node']['edge_liked_by']['count']
            list_like.append(like)
            comment = data_media_photo[data_caption]['node']['edge_media_to_comment']['count']
            list_comment.append(comment)
        
        doc = dict(
            shortcode = list_shortcode,
            like = list_like,
            comment = list_comment
        )
        return doc
    

    def influencer_classification(username):
        count_followers = KNN_Classifier.get_data_profile(username)
        count_followers = count_followers['count_follower']
        if count_followers > 1000000:
            jenis = 'Mega Influencer'
        elif 1000000>count_followers>100000:
            jenis = 'Macro Influencer'
        elif 100000>count_followers>10000:
            jenis = 'Micro Influencer'
        else:
            jenis = "Nano Influencer"
        return jenis

    def engagement_rate(username):
        data_profile = KNN_Classifier.get_img_post(username)
        for_follower = KNN_Classifier.get_data_profile(username)
        followers = for_follower['count_follower']
        list_like = data_profile['like']
        list_comment = data_profile['comment']
        list_engagement_rate = []
        for data in range (len(list_like)):
            engagement_rate = ((list_like[data]+list_comment[data])/followers)*100
            engagement_rate = round(engagement_rate, 2)
            list_engagement_rate.append(engagement_rate)
        return list_engagement_rate
 