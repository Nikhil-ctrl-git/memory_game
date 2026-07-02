# app.py
import streamlit as st
import random

st.set_page_config(page_title="🎴 Memory Match", page_icon="🎴", layout="centered")

SYMBOLS=["🍎","🍌","🍇","🍒","🍉","🍓","🍑","🥝"]

st.markdown("""
<style>
.stApp{background:linear-gradient(135deg,#0f172a,#1e293b,#111827);}
h1{text-align:center;color:white;}
p,label{color:white;}
[data-testid="stMetric"]{background:#3A3A3A;padding:10px;border-radius:12px;}
div.stButton>button{
width:72px;height:72px;border-radius:16px;
font-size:32px;background:#808080;color:white;
border:2px solid #334155;transition:.2s;
}
div.stButton>button:hover{transform:scale(1.05);border-color:#38bdf8;}
.blank{width:72px;height:72px;}
</style>
""",unsafe_allow_html=True)

def new_game():
    cards=SYMBOLS*2
    random.shuffle(cards)
    st.session_state.cards=cards
    st.session_state.matched=[False]*16
    st.session_state.selected=[]
    st.session_state.current_player=1
    st.session_state.scores={1:0,2:0}
    st.session_state.awaiting=False

if "cards" not in st.session_state:
    new_game()

def handle_click(i):
    if st.session_state.awaiting:return
    if st.session_state.matched[i] or i in st.session_state.selected:return
    if len(st.session_state.selected)>=2:return
    st.session_state.selected.append(i)
    if len(st.session_state.selected)==2:
        a,b=st.session_state.selected
        if st.session_state.cards[a]==st.session_state.cards[b]:
            st.session_state.matched[a]=True
            st.session_state.matched[b]=True
            st.session_state.scores[st.session_state.current_player]+=1
            st.session_state.selected=[]
            st.rerun()
        else:
            st.session_state.awaiting=True

st.title("🎴 Memory Match")
c1,c2,c3=st.columns(3)
c1.metric("Player 1",st.session_state.scores[1])
c2.metric("Turn",f"Player {st.session_state.current_player}")
c3.metric("Player 2",st.session_state.scores[2])
st.divider()

offset=[0,1,0,1]
for r in range(4):
    cols=st.columns([0.5,1,1,1,1])[1:] if offset[r] else st.columns(4)
    for c in range(4):
        idx=r*4+c
        if st.session_state.matched[idx]:
            cols[c].markdown('<div class="blank"></div>',unsafe_allow_html=True)
            continue
        label=st.session_state.cards[idx] if idx in st.session_state.selected else "❓"
        cols[c].button(label,key=f"b{idx}",on_click=handle_click,args=(idx,),disabled=st.session_state.awaiting)

if st.session_state.awaiting:
    st.warning(f"No Match! Player {st.session_state.current_player}'s turn ends.")
    if st.button("Continue ➡️",use_container_width=True):
        st.session_state.selected=[]
        st.session_state.awaiting=False
        st.session_state.current_player=2 if st.session_state.current_player==1 else 1
        st.rerun()

if all(st.session_state.matched):
    st.success("🎉 Game Over!")
    p1,p2=st.session_state.scores[1],st.session_state.scores[2]
    if p1>p2:
        st.balloons();st.header("🏆 Player 1 Wins!")
    elif p2>p1:
        st.balloons();st.header("🏆 Player 2 Wins!")
    else:
        st.header("🤝 It's a Tie!")
    if st.button("🔄 Play Again",use_container_width=True):
        new_game()
        st.rerun()

