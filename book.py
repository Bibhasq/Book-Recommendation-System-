from flask  import Flask,render_template,request
import pickle
import numpy as np

top_50 = pickle.load(open('top_50.pkl', 'rb'))
final_pivot = pickle.load(open('final_pivot.pkl', 'rb'))
similarity_score = pickle.load(open('similarity_score.pkl', 'rb'))
final_ratings = pickle.load(open('final_ratings.pkl', 'rb'))
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('book_recommender_index.html',
                           book_name = list(top_50['book_title'].values),
                           image=list(top_50['image_url_m'].values),
                           author=list(top_50['book_author'].values),
                           ratings=list(top_50['average_ratings'].values)
                           )

@app.route('/recommend_books',methods = ['POST'])
def recommend():
    user_ip = request.form.get('user_ip')
    selected_book = request.form.get('book_name')
    value = user_ip or selected_book
    indexing = final_pivot.index.get_loc(value)  # taking the index position
    similar_items = sorted(list(enumerate(similarity_score[indexing])), key=lambda x: x[1], reverse=True)[1:6]

    # Filter final_ratings to get rows where book_title is in final_pivot.index[i[0]] for i in some_iterable
    filtered_df = final_ratings[final_ratings['book_title'].isin([final_pivot.index[i[0]] for i in similar_items])]

    # Remove duplicates based on book_title, keeping the first occurrence
    filtered_df = filtered_df.drop_duplicates(['book_title']).drop(columns=['isbn', 'year_of_publication', 'user_id', 'publisher'])

    data = filtered_df[['book_title','book_author','image_url_m','number_of_ratings']].values.tolist()
    return render_template('recommend.html',data= data , user_ip = value)

if __name__ == '__main__':
    app.run(debug = True , port=5001)
