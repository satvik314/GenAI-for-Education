from educhain import qna_engine
from dotenv import load_dotenv
load_dotenv()

url_mcqs = qna_engine.generate_mcqs_from_data(
        source="https://en.wikipedia.org/wiki/Butterfly_effect",
        source_type="url",
        num=5
    )

print(url_mcqs)
## MCQList(questions=[MultipleChoiceQuestion(question='What is the butterfly effect?', answer='A phenomenon where small changes in initial conditions can lead to large-scale consequences.', explanation='The butterfly effect refers to the sensitive dependence on initial conditions, where a small change in a state of a deterministic nonlinear system can result in significant differences in a later state.', options=['A phenomenon where small changes in initial conditions can lead to large-scale consequences.', 'A method for accurately predicting weather patterns.', 'A type of chaos theory that applies only to mathematical models.', 'A term used to describe the behavior of butterflies in nature.']), MultipleChoiceQuestion(question='Who is closely associated with the concept of the butterfly effect?', answer='Edward Norton Lorenz', explanation="Edward Norton Lorenz, a mathematician and meteorologist, is credited with popularizing the term 'butterfly effect' through his work on chaos theory and weather prediction.", options=['Henri Poincaré', 'Edward Norton Lorenz', 'Norbert Wiener', 'James Annan']), MultipleChoiceQuestion(question='What was the metaphor originally used by Lorenz before adopting the butterfly?', answer='A seagull causing a storm', explanation='Lorenz originally used the metaphor of a seagull causing a storm but later adopted the more poetic butterfly metaphor.', options=['A hummingbird causing a hurricane', 'A seagull causing a storm', 'A dragonfly creating a tornado', 'A moth influencing a cyclone']), MultipleChoiceQuestion(question='In what year did Lorenz publish his seminal paper on the butterfly effect?', answer='1963', explanation="Lorenz published his highly cited paper titled 'Deterministic Nonperiodic Flow' in 1963, which introduced the butterfly effect in the context of chaos theory.", options=['1963', '1972', '1969', '1952']), MultipleChoiceQuestion(question='What is one of the practical consequences of the butterfly effect in chaotic systems?', answer='Small perturbations can lead to large-scale changes over time.', explanation='The butterfly effect demonstrates that in chaotic systems, even minor changes in initial conditions can result in vastly different outcomes, making long-term prediction difficult.', options=['Events can be predicted with complete accuracy.', 'Small perturbations can lead to large-scale changes over time.', 'Weather patterns are entirely deterministic.', 'Initial conditions have no impact on future states.'])])
url_mcqs.show()

