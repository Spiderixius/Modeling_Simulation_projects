import random as rnd
import numpy as np
from itertools import islice

def main():
    print("Random Number Generation using LCG")
    generate_lcg(100)
    generate_lcg_randu(100)
    run_tests()


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

def run_tests():
    input_file = "lgc_output.txt"
    test_name = "LINEAR CONGRUENTIAL GENERATOR"
    print("---------KS_TEST-----------")
    first_100_values = collect_first_100_samples_in_data_set(input_file)
    first_100_values.sort()
    ks_result = kolmogorov_smirnov_test(first_100_values,1,100)
    ks_significance_test(ks_result,100, 0.1)
    ks_significance_test(ks_result,100, 0.05)
    ks_significance_test(ks_result,100, 0.01)
    print ("Kolmogorov-Smirnov Test Result for D-Value: " + str(ks_result))
    print ("")


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

if __name__ == "__main__":
    main()
