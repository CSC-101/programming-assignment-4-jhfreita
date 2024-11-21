import data
import build_data
import county_demographics
from data import CountyDemographics
from build_data import convert_county
full_data = build_data.get_data()
sample_file = input("Enter a file name: ")
open(sample_file, "r")
# The following function is designed to read each line in a file and do various things depending on
# its contents. If the line requests the total population of some data, the population of the counties in
# the data will be printed. If the line requests filter by state, the data will be filtered accordingly, and the counties
# to be included in the filtered data will be displayed unless there are too many counties to be displayed.
# If the line requests filtering by a certain attribute being greater or less than a number, a list of counties
# meeting that requirement will be printed. If the line requests a certain percent or total population of all the counties
# in a set of data, that will be returned. Lastly, if an error occurs due to a line, the user should be notified.
# Error control is admittedly compromised, as I have been behind on my assignments lately. Sorry
with open(sample_file, "r") as file:
        first_line = file.readline().strip()
        data = full_data
        def display(county):
            print(f"County Name: {county.county}, State: {county.state}")
            print("\nPopulation:")
            for key, value in county.population.items():
                print(f"{key}: {value}")
            print("\nAge:")
            for key, value in county.age.items():
                print(f"{key}: {value}%")
            print("\nEducation:")
            for key, value in county.education.items():
                print(f"{key}: {value}%")
            print("\nEthnicities:")
            for key, value in county.ethnicities.items():
                print(f"{key}: {value}%")
            print("\nIncome:")
            for key, value in county.income.items():
                print(f"{key}: {value}")
        def population_total(CountyDemographics_list: list):
            population_list = [i.population for i in CountyDemographics_list]
            total_population = 0
            for i in range(len(CountyDemographics_list)):
                total_population = total_population + CountyDemographics_list[i].population['2014 Population']
            return total_population
        def filter_by_attribute1(counties: list, attribute: str, specification, threshold: str):
            modified_list = [i for i in counties if getattr(i, attribute)[specification] > float(threshold)]
            return modified_list
        def filter_by_attribute2(counties: list, attribute: str, specification, threshold: str):
            modified_list = [i for i in counties if getattr(i, attribute)[specification] < float(threshold)]
            return modified_list
        if first_line[:16] == "population-total":
            print("2014 Population:", population_total(data))
        elif first_line[:9] == "filter-gt":
            parts = first_line.split(":", 2)
            part1 = parts[0]
            part4 = parts[2]
            part2, part3 = parts[1].split(".", 1)
            part5 = part2.lower()
            raw_list = filter_by_attribute1(data, part5, part3, part4)
            presentation_list = [display(i) for i in raw_list]
            print(presentation_list)
        elif first_line[:9] == "filter-lt":
            parts = first_line.split(":", 2)
            part1 = parts[0]
            part4 = parts[2]
            part2, part3 = parts[1].split(".", 1)
            part5 = part2.lower()
            raw_list = filter_by_attribute2(data, part5, part3, part4)
            presentation_list = [display(i) for i in raw_list]
            print(presentation_list)
        else:
            if first_line[:12] == "filter-state":
                parts = first_line.split("-", 1)
                part1 = parts[0]
                part2, part3 = parts[1].split(":", 1)
                data = [i for i in full_data if i.state == part3]
                if len(data) > 6:
                    print(len(data), "entries")
                else:
                    presentation_list = [display(i) for i in data]
                    print(presentation_list)
            for line in file:
                try:
                    line = line.rstrip("\n")
                    if line[:16] == "population-total":
                        print("2014 Population:", population_total(data))
                    elif line[:9] == "filter-gt":
                        parts = line.split(":", 2)
                        part1 = parts[0]
                        part4 = parts[2]
                        part2, part3 = parts[1].split(".", 1)
                        print(filter_by_attribute1(data, part2, part3, part4))
                    elif line[:9] == "filter-lt":
                        parts = line.split(":", 2)
                        part1 = parts[0]
                        part4 = parts[2]
                        part2, part3 = parts[1].split(".", 1)
                        print(filter_by_attribute2(data, part2, part3, part4))
                    else:
                        parts = line.split(":", 1)
                        part1 = parts[0]
                        part2, part3 = parts[1].split(".", 1)
                        part4 = part2.lower()
                        def population_by_attribute(counties: list, attribute: str, specification: str):
                            population_list = [
                                0.01 * i.population['2014 Population'] * getattr(i, attribute)[specification]
                                for i in counties]
                            total_population = sum(population_list)
                            return total_population
                        if part1 == "population":
                            print("2014", part2, ".", part3, ":", population_by_attribute(data, part4, part3))
                        if part1 == "percent":
                            print("2014", part2, ".", part3, ":", 100 * population_by_attribute(data, part4, part3)/population_total(data))
                except ValueError:
                    print("An error occurred")
