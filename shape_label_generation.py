from syntax import AtomicEntity, TransformedDescriptor, Transformer, Entity
import random

circle = AtomicEntity('circle')
square = AtomicEntity('square')
triangle = AtomicEntity('triangle')

inside_of = Transformer('inside_of', Entity, TransformedDescriptor)
left_of = Transformer('left_of', Entity, TransformedDescriptor)

atomic_entities = [circle, square, triangle]
transformer_descriptors = [inside_of, left_of]

def generate_label(max_depth=3, complexity=0.2, restrict = False):
    if max_depth == 0 or random.random() > complexity or restrict:
        return random.choice(atomic_entities)
    
    trans = random.choice(transformer_descriptors)
    
    restrict = True if trans == inside_of else False
    return trans(generate_label(restrict=restrict))(generate_label(max_depth - 1, complexity))

if __name__ == '__main__':
    for i in range(100):
        print(len(generate_label(max_depth=40,complexity=0.5).linear_rep().split()))
    