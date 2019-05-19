"""
This file is probably only needed once to prompt manual clean-up of data (entries where Review=True)
"""

import pandas as pd
import logging
pd.set_option('display.max_colwidth', -1)
pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)
logging.basicConfig(filename='DataFrames/manual_review.log', level=logging.DEBUG, format="%(asctime)s %(message)s")


def read_files():
    which_data = input("Read in 'c'leaned data or 'o'riginal data?")
    if which_data == 'o':
        concerts_df = pd.read_csv("DataFrames/concerts_df.csv")
        meta_information_df = pd.read_csv("DataFrames/meta_information_df.csv")
        musical_pieces_df = pd.read_csv("DataFrames/musical_pieces_df.csv")
        # Currently not using other information due to confusion
        # other_information_df = pd.read_csv("DataFrames/other_information_df.csv").T
        pauses_df = pd.read_csv("DataFrames/pauses_df.csv", index_col=0)
        concerts_df.rename(columns={"Unnamed: 0": "Num"}, inplace=True)
        meta_information_df.rename(columns={"Unnamed: 0": "Num"}, inplace=True)
        musical_pieces_df.rename(columns={"Unnamed: 0": "Num"}, inplace=True)
    if which_data == 'c':
        concerts_df = pd.read_csv("DataFrames/concerts_df.csv")
        meta_information_df = pd.read_csv("DataFrames/meta_information_df_cleaned.csv")
        musical_pieces_df = pd.read_csv("DataFrames/musical_pieces_df_cleaned.csv", encoding='windows-1252')
        pauses_df = pd.read_csv("DataFrames/pauses_df_cleaned.csv")

    print("Welcome to manually reviewing the McVeigh dataframe! "
          "There are {} records to clean up. \n"
          "_________________________________________________________________________________________"
          "\n".format(len(meta_information_df[meta_information_df["REVIEW"] == True])))

    # For every concert programme that is flagged for review in meta_information, give all information and ask
    # for corrections.
    programmes_for_review = meta_information_df[meta_information_df["REVIEW"] == True]
    for programme_number in programmes_for_review["No"]:
        logging.warning("Programme number " + str(programme_number))
        print("1. Entire information was: ", concerts_df[concerts_df["No"] == programme_number]["Programme"].to_string())
        print("Meta information is: \n", meta_information_df[meta_information_df["No"] == programme_number])
        logging.debug("Meta information")
        correction = ""
        while correction != 'x':
            correction = input("Please input 'ch Row Column New_value | del Row | ins Numbering' to change values,"
                               " cp Row to append a copy of that row to table "
                               "or 'x' if you don't have any more corrections.")
            if correction and correction != 'x':
                correction = correction.split()
                typ = correction[0]
                tup = tuple(correction[1:])
                print(typ, tup)
                if typ == "ins":
                    new_row = pd.DataFrame.from_dict({"No": [programme_number], "Num": [tup[0]]})
                    meta_information_df = meta_information_df.append(new_row, ignore_index=True)
                    logging.info("Insert " + str(programme_number) + " " + str(tup[0]))
                if typ == "del":
                    meta_information_df = meta_information_df.drop(int(tup[0]))
                    logging.info("Delete " + str(tup[0]))
                if typ == "ch":
                    meta_information_df.set_value(int(tup[0]), tup[1], str(tup[2]))
                    logging.info("Change " + str(tup[0]) + " " + str(tup[1]) + " " + str(tup[2]))
                if typ == "cp":
                    old_row = meta_information_df.ix[int(tup[0])]
                    meta_information_df = meta_information_df.append(old_row, ignore_index=True)
                    logging.info("Copy " + str(tup[0]))
            print("Meta information is now: \n", meta_information_df[meta_information_df["No"] == programme_number])

        print("2. Entire information was: ", concerts_df[concerts_df["No"] == programme_number]["Programme"].to_string())
        print("Musical pieces information is: \n", musical_pieces_df[musical_pieces_df["No"] == programme_number])
        logging.debug("Musical pieces information")
        correction = ""
        while correction != 'x':
            correction = input("Please input 'ch Row Column New_value | del Row | ins Numbering | cp Row' "
                               "to change values "
                               "or 'x' if you don't have any more corrections.")
            if correction and correction != 'x':
                correction = correction.split()
                typ = correction[0]
                tup = tuple(correction[1:])
                print(typ, tup)
                if typ == "ins":
                    new_row = pd.DataFrame.from_dict({"No": [programme_number], "Num": [tup[0]]})
                    musical_pieces_df = musical_pieces_df.append(new_row, ignore_index=True)
                    logging.info("Insert " + str(programme_number) + " " + str(tup[0]))
                if typ == "del":
                    musical_pieces_df = musical_pieces_df.drop(int(tup[0]))
                    logging.info("Delete " + str(tup[0]))
                if typ == "ch":
                    musical_pieces_df.set_value(int(tup[0]), tup[1], str(tup[2]))
                    logging.info("Change " + str(tup[0]) + " " + str(tup[1]) + " " + str(tup[2]))
                if typ == "cp":
                    old_row = musical_pieces_df.ix[int(tup[0])]
                    musical_pieces_df = musical_pieces_df.append(old_row, ignore_index=True)
                    logging.info("Copy " + str(tup[0]))
            print("Musical pieces information is now: \n", musical_pieces_df[musical_pieces_df["No"] == programme_number])

        print("3. Entire information was: ", concerts_df[concerts_df["No"] == programme_number]["Programme"].to_string())
        print("Pause information is: \n", pauses_df[pauses_df["No"] == programme_number])
        logging.debug("Pause information")
        correction = ""
        while correction != 'x':
            correction = input("Please input 'ch Row Column New_value | del Row | ins Numbering' to change values "
                               "or 'x' if you don't have any more corrections.")
            if correction and correction != 'x':
                correction = correction.split()
                typ = correction[0]
                tup = tuple(correction[1:])
                print(typ, tup)
                if typ == "ins":
                    new_row = pd.DataFrame.from_dict({"No": [programme_number], "Num": [tup[0]]})
                    pauses_df = pauses_df.append(new_row, ignore_index=True)
                    logging.info("Insert " + str(programme_number) + " " + str(tup[0]))
                if typ == "del":
                    pauses_df = pauses_df.drop(int(tup[0]))
                    logging.info("Delete " + str(tup[0]))
                if typ == "ch":
                    pauses_df.set_value(int(tup[0]), tup[1], str(tup[2]))
                    logging.info("Change " + str(tup[0]) + " " + str(tup[1]) + " " + str(tup[2]))
                if typ == "cp":
                    old_row = pauses_df.ix[int(tup[0])]
                    pauses_df = pauses_df.append(old_row, ignore_index=True)
                    logging.info("Copy " + str(tup[0]))
            print("Pause information is now: \n", pauses_df[pauses_df["No"] == programme_number])

        sav = input("Do you want to save the changes? 'n' if not otherwise by default yes.")
        if sav != 'n':
            # Set REVIEW to False so it doesn't get back to cleanup
            meta_information_df.loc[meta_information_df["No"] == int(programme_number), "REVIEW"] = False
            print("\n {} records remain in clean up. \n"
                  "_________________________________________________________________________________________"
                  "\n".format(len(meta_information_df[meta_information_df["REVIEW"] == True])))

            # Save the changes.
            meta_information_df.to_csv("DataFrames/meta_information_df_cleaned.csv", index=False)
            musical_pieces_df.to_csv("DataFrames/musical_pieces_df_cleaned.csv", index=False)
            pauses_df.to_csv("DataFrames/pauses_df_cleaned.csv", index=False)
            logging.info("Saving record.")
        else:
            print("Not saving.\n")
            logging.info("Not saving.")


if __name__ == "__main__":
    read_files()
