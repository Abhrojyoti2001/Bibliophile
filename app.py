from helper import Help
import pickle
import streamlit as st


hp = Help()
st.sidebar.title('Bibliophile')
books = pickle.load(open('model/books.pkl', 'rb'))
add_select_box = st.sidebar.selectbox("Select a option", ['Recommendation of books', 'Find books'])

if add_select_box == 'Recommendation of books':
    selected_book = st.sidebar.selectbox("Type or select a book from the dropdown", books['title'])
    selected_number = st.sidebar.radio("How many books are you want for recommendation?", (2, 4, 6, 8, 10))

    if st.sidebar.button("Show Recommendation"):
        title_list, authors_list, year_list, image_url_list, rating_list = hp.fetch_data(selected_book, selected_number)
        for i in range(selected_number):
            col1, col2 = st.beta_columns(2)
            with col1:
                st.image(image_url_list[i], width=200)
            with col2:
                st.subheader(title_list[i])
                text1 = '<p style="font-family:Times; color:Cyan; font-size: 20px;">**{}**</p>'.format(authors_list[i])
                st.markdown('written by' + text1, unsafe_allow_html=True)
                text2 = '<p style="font-family:Times; color:Red; font-size: 20px;">**{}**</p>'.format(year_list[i])
                st.markdown('publication on' + text2, unsafe_allow_html=True)
                text3 = '<p style="font-family:Times; color:Green; font-size: 20px;">**{}**</p>'.format(rating_list[i])
                st.markdown("book's ratting is" + text3, unsafe_allow_html=True)

else:
    selected_radio = st.sidebar.radio("How will you find?", ('by Title', 'by Authors', 'by Publication year'))
    if selected_radio == 'by Title':
        selected_option = st.sidebar.selectbox("Type or select a book from the dropdown", books['title'])
    elif selected_radio == 'by Authors':
        selected_option = st.sidebar.selectbox("Type or select a book from the dropdown", books['authors'].unique())
    else:
        selected_option = st.sidebar.selectbox("Type or select a book from the dropdown", books['year'].unique())

    if st.sidebar.button("Go"):

        if selected_radio == 'by Title':
            col1, col2 = st.beta_columns(2)
            with col1:
                st.image(books[books['title'] == selected_option].image_url.values[0], width=200)
            with col2:
                st.header(selected_option)
                text1 = '<p style="font-family:Times; color:Cyan; font-size: 20px;">**{}**</p>'.format(books[books['title'] == selected_option].authors.values[0])
                st.markdown('written by' + text1, unsafe_allow_html=True)
                text2 = '<p style="font-family:Times; color:Red; font-size: 20px;">**{}**</p>'.format(books[books['title'] == selected_option].year.values[0])
                st.markdown('publication on' + text2, unsafe_allow_html=True)
                text3 = '<p style="font-family:Times; color:Green; font-size: 20px;">**{}**</p>'.format(books[books['title'] == selected_option].rating.values[0])
                st.markdown("book's ratting is" + text3, unsafe_allow_html=True)

        elif selected_radio == 'by Authors':
            result = len(books[books['authors'] == selected_option])
            if result > 10:
                loop_count = 10
            else:
                loop_count = result
            hp.update('authors', 1, result, loop_count, selected_option)

        else:
            result = len(books[books['year'] == selected_option])
            if result > 10:
                loop_count = 10
            else:
                loop_count = result
            hp.update('year', 1, result, loop_count, selected_option)
