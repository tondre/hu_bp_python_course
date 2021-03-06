import processes as proc
import molecules as mol
import logger as loggy

class Model(object):
    """
    Initializes the states and processes for the model and lets the processes update their corresponding states.
    """
    def __init__(self):
        self.states = {}
        self.processes = {}

        # initiate states
        self.ribosomes = {'Ribosomes': mol.Ribosome('Ribosomes', 'Ribosomes', 10)}
        self.mrnas = {'MRNA_{0}'.format(i): mol.MRNA(i, 'MRNA_{0}'.format(i), "UUUUUUUUUUAA") for i in xrange(50)}
        self.states.update(self.ribosomes)
        self.states.update(self.mrnas)
        #self.states.update({'MRNA_50': mol.MRNA(50, 'MRNA_50', "UUUGGCCUUUUUAA")})

        # initiate processes
        translation = proc.Translation(1, "Translation")
        translation.set_states(self.mrnas.keys(), self.ribosomes.keys())
        self.processes = {"Translation":translation}

        self.logger=loggy.Logger()  # create the logger object

    def step(self):
        """
        Do one update step for each process.

        """
        for p in self.processes:
            self.processes[p].update(self)

    def simulate(self, steps, log=True):
        """
        Simulate the model for some time.

        """

        for s in xrange(steps):
            self.step()
            if log: # This could be an entry point for further logging
                # print count of each protein to the screen
                #print '\r{}'.format([len(self.states[x]) for x in self.states.keys() if "Protein_" in x]),
                self.logger.add_step(self.states.items()) # store the states of a timestep to the Logger object 

    def output(self): # wrapper: create the output data type after a simulation was done.  
        return self.logger.output() 

if __name__ == "__main__":
    c = Model()
    c.simulate(100, log=True)
    print c.output() # print the output data type of the Logger. Can be used for Plotting!!!

