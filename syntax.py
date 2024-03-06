class Entity:
    pass

class AtomicEntity(Entity):
    """Entity that doesn't isn't composed of other entities. Represents a single word"""
    def __init__(self, name):
        self.name = name
    
    def __repr__(self) -> str:
        return f"AtomicEntity({self.name})"
    
    def __str__(self) -> str:
        return self.name
    
    def linear_rep(self):
        return self.name

class DescriptedEntity(Entity):
    """Entity that is made from a descriptor and another entity """
    def __init__(self, entity: Entity, descriptor: "Descriptor"):
        self.entity = entity
        self.descriptor = descriptor

    def __repr__(self) -> str:
        return f"DescriptedEntity({self.entity}, {self.descriptor})"
    
    def __str__(self) -> str:
        return f"{self.descriptor.__str__()}({self.entity.__str__()})"
    
    def linear_rep(self):
        if type(self.descriptor) == TransformedDescriptor:
            return self.entity.linear_rep() + ' ' +self.descriptor.linear_rep()
        return self.descriptor.linear_rep() + ' ' + self.entity.linear_rep()
    
class CompositeEntity(Entity):
    """Entity that is made from two or more entities using a connective word"""
    def __init__(self, composer: "Composer", entity_list: list[Entity]):
        self.composer = composer
        self.entity_list = entity_list

    def __str__(self) -> str:
        return f'{self.composer.__str__()}({", ".join(arg.__str__() for arg in self.entity_list)})'
    
    def linear_rep(self):
        return self.entity_list[0].linear_rep() + ' ' + self.composer.linear_rep() + ' ' + self.entity_list[1].linear_rep()

class Action:
    def __call__(self, *args):
        return AtomicProcess(self, *args)
    
class AtomicAction(Action):
    """actions that aren't made up of other actions or descriptors, like 'eat', 'see', etc. """
    def __init__(self, name, args_types):
        self.name = name
        self.args_types = args_types
    
    def __str__(self) -> str:
        return self.name
    
    def __repr__(self) -> str:
        return
    
    def linear_rep(self):
        return self.name
    

class DescriptedAction(Action):
    """Action that is made from a descriptor and another action """
    def __init__(self, action: Action, descriptor: "Descriptor"):
        self.action = action
        self.descriptor = descriptor

    def __repr__(self) -> str:
        return f"DescriptedAction({self.action}, {self.descriptor})"
    
    def __str__(self) -> str:
        return f"{self.descriptor.__str__()}({self.action.__str__()})"
    
    def linear_rep(self):
        return self.descriptor.linear_rep() + ' ' + self.action.linear_rep()

class CompositeAction(Action):
    """Action that is made from two or more actions using a connective word"""
    def __init__(self, composer: "Composer", action_list: list[Entity]):
        self.composer = composer
        self.action_list = action_list

    def __str__(self) -> str:
        return f'{self.composer.__str__()}({", ".join(arg.__str__() for arg in self.action_list)})'
    
    def linear_rep(self):
        return self.action_list[0].linear_rep() + ' ' + self.composer.linear_rep() + ' ' + self.action_list[1].linear_rep()
 

class Descriptor:
    def __call__(self, phrase):
        if isinstance(phrase, Entity):
            return DescriptedEntity(entity=phrase, descriptor=self)
        
        if isinstance(phrase, Action):
            return DescriptedAction(action=phrase, descriptor=self)
    
class AtomicDescriptor(Descriptor):
    def __init__(self, name):
        self.name = name
    
    def __str__(self) -> str:
        return self.name
    
    def __repr__(self) -> str:
        return f'Descriptor({self.name})'
    
    def linear_rep(self):
        return self.name

    
class TransformedDescriptor(Descriptor):
    def __init__(self, transformer: "Transformer", object):
        self.transformer = transformer
        self.object = object
    
    def __str__(self) -> str:
        return f"{self.transformer.__str__()}({self.object.__str__()})"
    
    def linear_rep(self):
        return self.transformer.linear_rep() + ' ' + self.object.linear_rep()

class CompositeDescriptor(Descriptor):
    def __init__(self, composer: "Composer", descriptor_list: list[Descriptor]):
        self.composer = composer
        self.descriptor_list = descriptor_list

    def __str__(self) -> str:
        return f'{self.composer.__str__()}({", ".join(arg.__str__() for arg in self.descriptor_list)})'
    
    def linear_rep(self):
        return self.descriptor_list[0].linear_rep() + ' ' + self.composer.linear_rep() + ' ' + self.descriptor_list[1].linear_rep()
    


class Process:
    pass

class AtomicProcess(Process):
    def __init__(self, action: Action, *action_args):
        self.action = action
        self.action_args = action_args

    def __str__(self):
        return f'{self.action.__str__()}({", ".join(arg.__str__() for arg in self.action_args)})'
    
    def linear_rep(self):
        return self.action_args[0].linear_rep() + ' ' + self.action.linear_rep() + ' ' + ' '.join(arg.linear_rep() for arg in self.action_args[1:])

class CompositeProcess(Process):
    def __init__(self, composer: "Composer", process_list: list[Process]):
        self.composer = composer
        self.process_list = process_list
    
    def __str__(self) -> str:
        return f'{self.composer.__str__()}({", ".join(arg.__str__() for arg in self.process_list)})'
    
    def linear_rep(self):
        return self.process_list[0].linear_rep() + ' ' + self.composer.linear_rep() + ' ' + self.process_list[1].linear_rep() 

class Composer:
    """ words like 'and', 'but', 'therfore', etc. """
    def __init__(self, name, arg_types):
        self.name = name
        self.arg_types = arg_types
    
    def __call__(self, *arg_list):
        if isinstance(arg_list[0], Entity):
            return CompositeEntity(self, arg_list)
        if isinstance(arg_list[0], Action):
            return CompositeAction(self, arg_list)
        if isinstance(arg_list[0], Process):
            return CompositeProcess(self, arg_list)
        
    def __str__(self):
        return self.name
    def _validate_args(self, arg_list):
        if [type(a) for a in arg_list] in self.arg_types:
            return True
        return False
    
    def linear_rep(self):
        return self.name

class Transformer:
    """ words like 'of', 'with', etc. for example, of(john) transforms john to a descriptive, 
    and with(john) transforms it to descriptive also.
    """
    def __init__(self, name, input_type: type, output_type: type):
        self.name = name
        self.input_type = input_type
        self.output_type = output_type

    def __str__(self) -> str:
        return self.name

    def __call__(self, input):
        return self.output_type(transformer=self, object=input)
    
    def linear_rep(self):
        return self.name
    
    

def pull_back_operator(action: Action, arguments:dict[int, Entity]):
    """given an action and arguments, returns"""
    pass


def main():
    john = AtomicEntity(name='John')
    nice = AtomicDescriptor(name='nicely')
    food = AtomicEntity(name='food')
    bill = AtomicEntity(name='Bill')
    enjoy = AtomicAction(name='enjoy',args_types=[Entity, Entity])
    And = Composer('and', [[Entity, Entity],[Action, Action],[Process,Process],[Descriptor, Descriptor]])
    eat = AtomicAction('eat', [Entity, Entity])
    of = Transformer('of', Entity, TransformedDescriptor)
    print(And(of(john)(food), bill))
    print(And(nice(eat),enjoy)(And(john,bill), food))
    print(And(nice(eat),enjoy)(And(john,bill), food).linear_rep())
if __name__ == "__main__":
    main()