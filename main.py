from FA_Algorithm.Repetittive_procedure import repProcedure as Algorithm

independent_runs = 40  #40
fa_iterations = 50  #100
fireflies_pop = 50  #100
dimensions = 30  #50


if __name__ == '__main__':
    """
    # This is for testing in console
    for i in range(independent_runs):
        print(Algorithm(fa_iterations, fireflies_pop, dimensions).results(i, independent_runs))
    """
    # This is for exporting the results in a csv file
    from csv_export_fun import csv_export
    name_of_file = "Results/res_CEC10_Con/res_F7/FA_PSO_CEC10_Con_F7_fun.csv"  # needs to be in a string from ("name.csv")
    csv_export(independent_runs, name_of_file)
