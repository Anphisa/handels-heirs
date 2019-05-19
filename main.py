import pandas as pd
import numpy as np
from ProgrammeDecoder import ProgrammeDecoder


class Main(object):
    def __init__(self, filename):
        self.concerts_df = pd.read_csv(filename)
        meta_informations_df = pd.DataFrame()
        other_informations_df = pd.DataFrame()
        pauses_df = pd.DataFrame()
        musical_pieces_df = pd.DataFrame()

        print "Decoding concert information."
        self.concerts_df["DateTime"] = pd.to_datetime(self.concerts_df["Date"]+self.concerts_df["Time"],
                                                      format="%Y_%m_%d%H%M", errors="coerce")
        self.concerts_df = self.concerts_df.drop(["Date", "Day", "Time"], axis=1)

        print "Decoding concerts."
        # Iterating concert by concert
        for index, concert in self.concerts_df.iterrows():
            index += 1
            print "Decoding concert # ", index
            # The decoded programme has single dictionaries/tuples for every information
            prog = concert["Programme"]
            prog_dec = ProgrammeDecoder(prog)

            meta_information_df = pd.DataFrame.from_dict(prog_dec.meta_information, orient="index").transpose()
            meta_information_df["No"] = index
            meta_informations_df = pd.concat([meta_informations_df, meta_information_df])

            other_information_df = pd.DataFrame.from_records(prog_dec.other_infos)
            other_information_df["No"] = index
            other_informations_df = pd.concat([other_informations_df, other_information_df])

            pauses = pd.DataFrame(list(prog_dec.pauses)).T
            pauses["No"] = index
            pauses_df = pd.concat([pauses_df, pauses])

            musical_pieces = pd.DataFrame.from_dict(prog_dec.content_dict, orient='index')
            musical_pieces["No"] = index
            musical_pieces_df = pd.concat([musical_pieces_df, musical_pieces])

        print "Now expanding instruments and performers."
        musical_pieces_df = musical_pieces_df.fillna(value=0)

        # Expanding lists of instruments and performers (if two performers are listed)
        res = musical_pieces_df.set_index(['Composer', 'From', 'Genre', 'No', 'Title_of_Piece'])['Instrument'].apply(pd.Series).stack()
        res = res.reset_index()
        res.columns = ['Composer', 'From', 'Genre', 'No', 'Title_of_Piece', 'Instrument_Num', 'Instrument']
        res.to_csv("res.csv")

        res2 = musical_pieces_df.set_index(['Composer', 'From', 'Genre', 'No', 'Title_of_Piece'])['Performer'].apply(pd.Series).stack()
        res2 = res2.reset_index()
        res2.columns = ['Composer', 'From', 'Genre', 'No', 'Title_of_Piece', 'Performer_Num', 'Performer']
        res2.to_csv("res2.csv")

        musical_pieces_df = pd.concat([res, res2["Performer"]], axis=1)

        # Saving dataframes for further processing (cleanup etc)
        self.concerts_df.to_csv("DataFrames/concerts_df.csv")
        meta_informations_df.to_csv("DataFrames/meta_information_df.csv")
        other_informations_df.to_csv("DataFrames/other_information_df.csv")
        pauses_df.to_csv("DataFrames/pauses_df.csv")
        musical_pieces_df.to_csv("DataFrames/musical_pieces_df.csv")

        # print "Now grouping content."
        #
        # composer_genre_of_piece = musical_pieces_df.ix[musical_pieces_df["Instrument_Num"] == 0]
        #
        # self.composer_group = composer_genre_of_piece.groupby(musical_pieces_df['Composer'].str.upper()).count()
        # self.instrument_group = musical_pieces_df.groupby(musical_pieces_df['Instrument'].str.upper()).count()
        # self.genre_group = composer_genre_of_piece.groupby(musical_pieces_df['Genre'].str.upper()).count()
        # self.performer_group = musical_pieces_df.groupby(musical_pieces_df['Performer'].str.upper()).count()
        #
        # self.composer_group.to_csv("Groups/composers_group_out.csv")
        # self.instrument_group.to_csv("Groups/instruments_group_out.csv")
        # self.genre_group.to_csv("Groups/genres_group_out.csv")
        # self.performer_group.to_csv("Groups/performers_group_out.csv")

if __name__ == "__main__":
    main = Main("MUS-McVeigh_Calendar_csv_Ver_02_29_Dec_2014.csv")