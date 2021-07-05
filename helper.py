import pickle
import streamlit as st


class Help:

    def __init__(self):
        self.books = pickle.load(open('model/books.pkl', 'rb'))

    def fetch_data(self, book, n):
        title_list = self.books[self.books['title'] == book]['similar_books'].values[0]
        authors_list = []
        year_list = []
        image_url_list = []
        rating_list = []
        for i in range(n):
            authors_list.append(self.books[self.books['title'] == title_list[i]].authors.values[0])
            year_list.append(self.books[self.books['title'] == title_list[i]].year.values[0])
            image_url_list.append(self.books[self.books['title'] == title_list[i]].image_url.values[0])
            rating_list.append(self.books[self.books['title'] == title_list[i]].rating.values[0])

        return title_list, authors_list, year_list, image_url_list, rating_list

    def update(self, col, counter, result,  loop_count, selected_option):
        self.col = col
        self.counter = counter
        self.result = result
        self.loop_count = loop_count
        self.selected_option = selected_option
        self.total_pages = 1 + self.result // 10
        self.load_books()

    def load_books(self):
        start = self.loop_count*(self.counter-1)
        if self.counter == self.total_pages:
            end = self.result
        else:
            end = self.loop_count*self.counter
        for i in range(start, end):
            col1, col2 = st.beta_columns(2)
            with col1:
                st.image(self.books[self.books[self.col] == self.selected_option].image_url.values[i], width=200)
            with col2:
                st.header(self.books[self.books[self.col] == self.selected_option].title.values[i])
                if self.col == 'authors':
                    text1 = '<p style="font-family:Times; color:Cyan; font-size: 20px;">**{}**</p>'.format(self.selected_option)
                    st.markdown('written by' + text1, unsafe_allow_html=True)
                    text2 = '<p style="font-family:Times; color:Red; font-size: 20px;">**{}**</p>'.format(self.books[self.books[self.col] == self.selected_option].year.values[i])
                    st.markdown('publication on' + text2, unsafe_allow_html=True)
                else:
                    text1 = '<p style="font-family:Times; color:Cyan; font-size: 20px;">**{}**</p>'.format(self.books[self.books[self.col] == self.selected_option].authors.values[i])
                    st.markdown('written by' + text1, unsafe_allow_html=True)
                    text2 = '<p style="font-family:Times; color:Red; font-size: 20px;">**{}**</p>'.format(self.selected_option)
                    st.markdown('publication on' + text2, unsafe_allow_html=True)
                text3 = '<p style="font-family:Times; color:Green; font-size: 20px;">**{}**</p>'.format(self.books[self.books[self.col] == self.selected_option].rating.values[i])
                st.markdown("book's ratting is" + text3, unsafe_allow_html=True)

        if self.result > 10:
            col1, col2, col3 = st.beta_columns(3)
            with col1:
                if self.counter > 1:
                    st.button("Previous", on_click=lambda: self.controller("Previous"))
            with col2:
                st.text(str(self.counter) + " page of " + str(self.total_pages))
            with col3:
                if self.counter <= self.result // 10:
                    st.button("NexT", on_click=lambda: self.controller("NexT"))

    def controller(self, btn):
        if btn == "NexT":
            self.counter += 1
        else:
            self.counter -= 1
        self.load_books()
