import pandas as pd
import altair as alt
from PIL import Image
import streamlit as st

image = Image.open('dna-logo.jpg')
st.image(image, use_column_width=True)

st.write(
    """
    # DNA Nucleotide Count Web App
    
    This app counts the Nucleotide composition of DNA Query!
    """
)

st.header('Enter DNA Sequence')
sequence_input = '>DNA Query\nGAACACTGGAGGCAAACAGGAAGGTGAAGAAGAACTTATCAGGACGGAAGGTCCTGTGCTCGGG\nGAACACTGGAGGCAAACAGGAAGGTGAAGAAGAACTTATCAGGACGGAAGGTCCTGTGCTCGGG\nGAACACTGGAGGCAAACAGGAAGGTGAAGAAGAACTTATCAGGACGGAAGGTCCTGTGCTCGGG\n'
sequence = st.text_area("Sequence input", sequence_input, height=250)
sequence = sequence.splitlines()
sequence = sequence[1:]
sequence = ''.join(sequence)

st.write(
    """
    ***
    """
)

st.header('INPUT (DNA QUERY)')
sequence

st.header('OUTPUT (DNA Nucleotide Count)')
st.subheader('1- Print dictionary')

def DNA_nucleotide_count(seq):
    d = dict([
        ('A', seq.count('A')),
        ('C', seq.count('C')),
        ('G', seq.count('G')),
        ('T', seq.count('T'))
    ])
    return d

X = DNA_nucleotide_count(sequence)
X
# X_label = list(X)
# X_values = list(X.values())

st.subheader('2- Print text')
st.write('There are ' + str(X['A']) + ' adenine (A)')
st.write('There are ' + str(X['C']) + ' cytosine (C)')    
st.write('There are ' + str(X['G']) + ' guanine (G)')    
st.write('There are ' + str(X['T']) + ' thymine (T)')    

st.subheader('3- Display Dataframe')
df = pd.DataFrame.from_dict(X, orient='index') #keys of the dict should be the index of dataframe
df = df.rename({0: 'count'}, axis='columns') #rename the 1st column as count
df.reset_index(inplace=True)
df = df.rename(columns= {'index': 'nucleotide'})
st.write(df)

st.subheader('4- Display Bar Chart')
chrt = alt.Chart(df).mark_bar().encode(
    x='nucleotide',
    y='count'
)
chrt = chrt.properties(
    width=alt.Step(80)
)
st.write(chrt)