import streamlit as st
from rouge import Rouge
from nltk.translate.bleu_score import sentence_bleu, SmoothingFunction

def evaluate_bleu(reference, candidate):
    reference_tokens = reference.split()
    candidate_tokens = candidate.split()
    # Use SmoothingFunction
    smoothie = SmoothingFunction().method4
    score = sentence_bleu([reference_tokens], candidate_tokens, smoothing_function=smoothie)
    return score

def evaluate_rouge(reference, candidate):
    rouge = Rouge()
    scores = rouge.get_scores(candidate, reference)
    return scores

def human_eval(human_evaluation):
    accuracy = human_evaluation/5 * 100
    return accuracy

rouge_results = 0
bleu_results = 0
human_evaluation_results = 0
def evaluations_tab():
    st.markdown(f"### BLEU Score")
    st.write(f"BLEU Score: {round(bleu_results, 2)}")
    st.markdown(f"### ROUGE Score")
    st.write(f"ROUGE-L Score: {rouge_results[0]['rouge-l'] if rouge_results != 0 else 0 }")
    st.markdown(f"### Human Feedback Reinforcement Learning")
    st.write(f"HFRL Score: {human_evaluation_results}")


st.subheader("Evaluations")

predicted_res = st.text_area("Chatbot response", )
actual_res = st.text_area("Ground truth")
human_evaluation = st.slider(
    'How well did the bot predict?',
    0.0, 5.0)

if st.button("Calculate Metrics") and predicted_res and actual_res:
    rouge_results = evaluate_rouge(actual_res, predicted_res)
    bleu_results = evaluate_bleu(actual_res, predicted_res)
    human_evaluation_results = human_eval(human_evaluation)



evaluations_tab()