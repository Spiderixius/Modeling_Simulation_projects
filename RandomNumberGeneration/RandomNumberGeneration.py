import random as rnd
import numpy as np
from itertools import islice

###########################################################################################################
### Source: https://tonypoer.io/2016/03/23/experimenting-with-linear-congruential-generators-in-python/ ###
###########################################################################################################
def main():
    num_observations = 10000
    print("Random Number Generation using LCG")
    generate_lcg(num_observations)
    generate_lcg_randu(num_observations)
    run_tests(num_observations)


################################
### Random Number Generators ###
################################

def generate_lcg(num_iterations):
    """
    Generate random numbers for as many iterations as specified.
    """

    # Initilize variables
    seed = 123456789
    a = 101427
    c = 321
    m = (2**16)

    # Counter for how many iterations has been run
    counter = 0
    outFile = open("lgc_output.txt", "w")

    # Perform number of iterations
    while counter < num_iterations:
        # Store value of each iteration
        seed = (a * seed + c) % m

        # Obtain each number in U[0, 1] by dividing seed_i by m
        writeValue = str(seed/m)

        # Write to file
        outFile.write(writeValue + "\n")
        #print (writeValue + "\n")

        counter = counter + 1

    outFile.close()
    #print("Successfully stored " + str(num_iterations) + " random numbers in file named: 'lgc_output.txt'.")


def generate_lcg_randu(num_iterations):
    """
    LCG using RANDU initial setting.
    """
    # Initilize variables
    seed = 123456789
    a = 65539
    c = 0
    m = (2**31)

    # Counter for how many iterations has been run
    counter = 0
    outFile = open("lgc_randu_output.txt", "w")

    # Perform number of iterations
    while counter < num_iterations:
        # Store value of each iteration
        seed = (a * seed + c) % m

        # Obtain each number in U[0, 1] by dividing seed_i by m
        writeValue = str(seed/m)

        # Write to file
        outFile.write(writeValue + "\n")
        #print (writeValue + "\n")

        counter = counter + 1

    outFile.close()


#######################
### Statistic Tests ###
#######################
# Contains:           ###################
#          - kolmogorov_smirnov_test    #
#          - runs_test_for_independence #
#########################################
def kolmogorov_smirnov_test(data_set, confidence_level, num_samples):
    """
    Using smirnov to test the uniform distribution of the random numbers
    """

    # Step 1: Rank data from smallest to largest, such that:
    # R(1) <= R(2) <= R(3) ... <= R(i)
    # The data to to analyze
    data_set.sort()

    # Step 2: Compute D+ and D-
    #D+ = max(i/N - R(i))
    d_plus = get_d_plus_value_for_KS_TEST(data_set, num_samples)
    print("D+ VALUE =" + str(d_plus))

    #D- = max(R(i) - (i-1)/n)
    d_minus = get_d_minus_value_for_KS_TEST(data_set, num_samples)
    print("D- VALUE (max)=" + str(d_minus))


    # Step 3: Compute D = max(D+, D-)
    d_value = max(d_plus, d_minus)
    print("D VALUE (max): " + str(d_value))

    # Step 4: Determine critical vale, using table
    # Step 5: Accept or reject Null hypothesis
    return d_value


def get_d_plus_value_for_KS_TEST( data_set, num_samples ):
    """
    Finds the D+ value for a KS test
    :param data_set: 100 values, must be a list of floats
    :return: the D-+Statistic for our data set
    """
    # D+ = max(i/N - R(i))
    d_plus_max = 0
    value_rank_i = 1

    # iterate through data set
    for value in data_set:
        # Do each D+ calculation, store it
        d_plus_i_value = ( (value_rank_i/num_samples) - value )

        # Check if it is highest D+ value yet
        if d_plus_i_value > d_plus_max:
            d_plus_max = d_plus_i_value

        # increment our "i" value
        value_rank_i = value_rank_i + 1

    # coming out of this loop, D+ = highest D+ value
    return d_plus_max


def get_d_minus_value_for_KS_TEST( data_set, num_samples ):
    """
    Finds the D- value for a KS test
    :param data_set: 100 values, must be a list of floats
    :return: the D- Statistic for our data set
    """
    # D- = max(R(i) - (i -1)/n)
    d_minus_max = 0
    value_rank_i = 1.0

    # iterate through data set
    for value in data_set:
        # Do each D+ calculation, store it
        substraction_value = ( (value_rank_i - 1.0)/num_samples )
        d_minus_i_value = value - substraction_value

        # Check if it is highest D+ value yet
        if d_minus_i_value > d_minus_max:
            d_minus_max = d_minus_i_value

        # increment our "i" value
        value_rank_i = value_rank_i + 1

    # coming out of this loop, D+ = highest D+ value
    return d_minus_max

def runs_test_for_independence( data_file, num_samples ):
    """
    Perform a runs test for independence for a set of random numbers
    :param data_set: A data set with 10,000 samples - should be a list, with all numbers floats
    :param num_samples: The number of samples to test
    :return: z-test statistic for our data set
    """
    # Note, every sequence begins and ends with "NO EVENT"
    # Run = Succession of similar events, followed by a different event
    # Run Length = Number of events that occur in the run
    # Number of runs = number of "runs" total
    # Two concerns: Num runs, length of runs
    # We're looking for:  Runs of larger and smaller numbers (increasing or decreasing)
    runLengths = { }       # The size of each run, in order
    numRuns = 0            # The number of runs overall
    runDirection = "none"  # We'll use "none", "up", and "down" to keep track

    with open( data_file, "r" ) as f:
        data_points = f.readlines()


   # for value in data_points:
    for value in range(0, (len(data_points)-1) ):

        # DEBUG
        thisValue = float(data_points[value])
        nextValue = float(data_points[value+1])
        # print "data_points[value] ::"+ str(thisValue)
        # print "dat_points[value+1] ::"+ str(nextValue)

        # If no change in direction we'll ignore
        if thisValue == nextValue:
            numRuns = numRuns             # numRums overall, doesn't change
            runDirection = runDirection   # runDirection doesn't change

        # Check if we have a NEW run, going UP
        elif thisValue < nextValue and runDirection != "up":
            numRuns = numRuns + 1         # We have a NEW run
            runDirection = "up"           # We have a NEW run direction
            runLengths[numRuns] = 1       # We have a NEW key in our dictionary, with value=1

        # Check if we have a CONTINUING run, going UP
        elif thisValue < nextValue and runDirection == "up":
            runLengths[numRuns] += 1      # increment the run length in our dictionary for current run
                                          # NumRuns doesn't change
                                          # runDirection doesn't change

        # Check if we have NEW run, going DOWN
        elif thisValue > nextValue and runDirection != "down":
            numRuns = numRuns + 1          # We have a NEW run
            runDirection = "down"          # We have a NEW run direction
            runLengths[numRuns] = 1        # We have a NEW key in our dictionary, with value=1

        # Check if we have a CONTINUING run, going DOWN
        elif thisValue > nextValue and runDirection == "down":
            runLengths[numRuns] += 1      # increment the run length in our dictionary for current run
                                          # NumRuns doesn't change
                                          # runDirection doesn't change

    # Leaving this loop, we should have a dictionary with our run numbers mapped to their lengths
    # We should also have a the number of runs

    # Now, calculate mean:  Mean = (2N-1)/3
    mean =  ( (2*num_samples - 1) / 3 )

    # And variance:  Variance = (16(N) - 29) / 90
    variance = ( ( 16*num_samples - 29) / 90 )

    # And we can use the mean & variance to calculate the Z-Test statistic
    z_statistic = ( (numRuns - mean) / np.sqrt(variance) )

    print ("Number of runs: " + str(numRuns))

    return z_statistic

######################
### Helper Methods ###
######################
def collect_first_100_samples_in_data_set( data_file ):
    """
    Takes a data file, with real number data points between [0,1) reads the first 100 values,
    then adds them to a dictionary as our return value
    :param data_file: A string - the name of the file to read in our current directory
    :return: A dictionary containing the first 100 values as floats
    """

    first_100_vals_as_FLOATS = []
    # grabs first 100 files, as strings with newline endpoints
    with open( data_file, "r" ) as f:
        first_100_vals_as_STRINGS = list(islice(f, 100))

    # transform all values to floats
    for val in first_100_vals_as_STRINGS:
        val = float(val)
        first_100_vals_as_FLOATS.append(val)

    return first_100_vals_as_FLOATS


##############################
##### Significance Tests #####
##############################
def ks_significance_test( d_statistic, num_observations, alpha_level ):
    """
    Perform Significance test for Kolmogorov-Smirnov
    Uses formulas from table A.7:  Discrete-Event System Simulation, by Banks and Carson, 1984
    :param d_statistic: The d-value we are testing
    :param num_observations: The number of observations in our data set
    :param alpha_level: The level of significance we are testing
    :return: result -- accept or reject
    """
    result = "FAIL TO REJECT null hypothesis"
    critical_value = 0

    if alpha_level == 0.1:
        critical_value = 1.22/np.sqrt(num_observations)
    elif alpha_level == 0.05:
        critical_value = 1.36/np.sqrt(num_observations)
    elif alpha_level == 0.01:
        critical_value = 1.63/np.sqrt(num_observations)
    else:
        print ("Invalid alpha level for KS test. Must be: 0.1, 0.05, or 0.01")

    if d_statistic > critical_value:
        result = "REJECT null hypothesis"
    print ("Alpha Level is: " + str(alpha_level))
    print ("D_statistic is: " + str(d_statistic))
    print ("Critical value is: " + str(critical_value))
    print ("Result is: " + result)
    print ("............................")

    return result

def z_score_lookup( z_score, significance_level, two_sided=True):
    """
    Performs a two-sided z-score lookup, for 0.8, 0.9, or 0.95 level of significance
    :param z_score: Z score to test
    :param significance_level: Significance level
    :return: String detailing our result
    """

    result = "FAIL TO REJECT null hypothesis"
    critical_value = 0.0
    confidence_80 = 1.282
    confidence_90 = 1.645
    confidence_95 = 1.96
    confidence_99 = 2.576

    # Assign confidence interval z-scores to our crit value
    if significance_level == 0.8:
        critical_value = confidence_80
    elif significance_level == 0.9:
        critical_value = confidence_90
    elif significance_level == 0.95:
        critical_value = confidence_95
    else:
        print ("Invalid significance level for z-lookup. Must be: 0.8, 0.9, or 0.95")

    # Need to adjust intervals if the test is one sided
    if two_sided == False:
        if critical_value == confidence_80:
            critical_value = 0.8416
        elif critical_value == confidence_90:
            critical_value = 1.282
        elif critical_value == confidence_95:
            critical_value = 1.645

    neg_crit_value = critical_value * (-1.0)

    #if z_score < 0:
     #  z_score = z_score * (-1)

    if ( two_sided and ( z_score <= neg_crit_value) or (critical_value <= z_score ) ):
        result = "REJECT null hypothesis"

    if ( not two_sided and z_score >= critical_value or z_score <= neg_crit_value):
        result = "REJECT null hypothesis"

    print ("Z score is: " + str(z_score))
    print ("Significance level is: " + str(significance_level))
    print ("Critical value is: " +str(critical_value))
    print ("Running two sided z-score lookup? -->" + str(two_sided))
    print ("")
    print ("Result is: " + result)
    print (".....................................")

    return result

##############################
### Method to handle tests ###
##############################
def run_tests(num_observations):
    """
    Run the Kolmogorov Smirnov and Runs tests.
    """

    input_file = "lgc_output.txt"
    test_name = "LINEAR CONGRUENTIAL GENERATOR"

    # Perform kolmogorov_smirnov_test
    print("---------KS_TEST-----------")
    first_100_values = collect_first_100_samples_in_data_set(input_file)
    first_100_values.sort()
    ks_result = kolmogorov_smirnov_test(first_100_values,1,100)
    ks_significance_test(ks_result,100, 0.1)
    ks_significance_test(ks_result,100, 0.05)
    ks_significance_test(ks_result,100, 0.01)
    print ("Kolmogorov-Smirnov Test Result for D-Value: " + str(ks_result))
    print ("")

    # Perform runs_test_for_independence
    # perform a runs test
    print ("---------RUNS_TEST-----------")
    runs_test_result = runs_test_for_independence( input_file, num_observations )
    print ("Runs Test Result Z-Score: " + str(runs_test_result))
    print ("")
    z_score_lookup(runs_test_result, 0.8, two_sided=True)
    z_score_lookup(runs_test_result, 0.9, two_sided=True)
    z_score_lookup(runs_test_result, 0.95, two_sided=True)
    print ("")

if __name__ == "__main__":
    main()
