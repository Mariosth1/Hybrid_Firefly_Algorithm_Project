This is a hybrid Firefly Algorithm running benchmark functions:
Mechanisms fetched from other nature inspired Algorithms are applied to solve FA's well-known problems
and also make it more robust, efficient, etc.

Specifically the mechanisms used to create schemes are:
1) The Fractal Diffusion of Stochastic Fractal Search
2) The PSO's movement


=======================================================================================================================
a) Inside _main_ you can set:
    1. fa_iterations = The iterations of FA in the Search Space.
    2. fireflies_pop = The population of the fireflies.
    3. independent_runs = The number of independent test runs of FA Algorithm.

    As preset _main_ prints the results in the console. The results are the fitness evaluation (Quality) and the
    allocation of the decision variables (Best Firefly Position).
    You can also choose if you want a csv file exported:
        Erase the comment with the csv function inside _main_ and change the "name_of_file" in a string ("name.csv") of
        your desire.

If you wish to change the FA parameters open the "FA_Algorithm.search_space.py":
    Inside the moveParticles function ("def moveFireflies"):
        self.alpha, beta0, gamma and delta

=======================================================================================================================
b) If you wish to change the fitness open the "FA_Algorithm.search_space.py":
    import your fitness function as fitness
    i.e.:
    "from Folder.yourFile import yourFitnessFunction as fitness"

The data are imported inside the objective function

The data and other parameters are imported in the "PSO_Algorithm.search_space.py":
    1. lower_bound = the lower bound of the decision variable, can be imported from data.
    2. upper_bound = the upper bound of the decision variable, can be imported from data.

    import from your data the 2 parameters
    i.e.:
    "from Folder.yourDataFile import lower_bound, upper_bound"

=======================================================================================================================
c) 3 Schemes created:
    1. FA - SFS (Firefly Algorithm with Stochastic Fractal Search, Fractal Diffusion Mechanism)
    2. FA - PSO (Firefly Algorithm with Particle Swarm Optimization's Movement)


    If you wish to change the scheme or run the simple FA, you can toggle them by changing the parameters to 'True':

    FRACTAL_DIFF = False
    PSO_MOVEMENT = False

    Which are located in the "FA_Algorithm.search_space.py" file.
=======================================================================================================================
d) Exploration - Exploitation:

    Its independent also returns the Average Xpl% and Xpt% of the Scheme.

    If you wish to plot a the Xpl and Xpt of the last Run, you can toggle them by changing the parameter to 'True':

    PLOTTING = False
