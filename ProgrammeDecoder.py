"""
This class decodes content of concert programmes as coded in McVeigh.
"""
import re

# Programme parts (first act, second act...)
all_parts = ("1:", "2:", "3:", "4:", "PART1", "PART2", "PART3", "PART4", "PARTS", "PARTS1-2", "PARTS1-3", "PARTS2-3")

# People
all_meta_people = ("COND", "LEAD", "DIR")

# Institutions
all_institutions = ("AAM")

# Instruments
all_instruments = ("BN", "BST_HN", "CL", "DB", "DBDR", "DBN", "DDR", "DRS", "FL", "FLDA", "GU", "HN", "HP", "HPD", "I",
                   "MAND", "MGL", "OB", "OBDA", "ORG", "PERFECT_PF", "PF", "PICC", "TELIOCORDONIZED_PF", "TENOR_OB",
                   "TINTINNABULA", "TPT", "VA", "VC", "VDA", "VDAG", "VN", "WIND_INSTR", "TRBN", "2CHOIR", "3CHOIR",
                   "4CHOIR", "V", "2V", "3V", "4V", "5V", "6V", "ORCH")

# Size
all_size_denoters = ("2CHOIR", "3CHOIR", "4CHOIR", "V", "2V", "3V", "4V", "5V", "6V", "ORCH")

# Genres
all_genres_of_music = ("ANTH", "CAM", "CH", "CN", "CNGR", "CNTE", "CT", "DIV", "DT", "FAV", "FP", "GL", "LSN", "MADR",
                      "NOTT", "O", "OV", "PANTALEON", "QNT", "QT", "RAUGH", "RECIT", "SALTERIO", "SER", "SG", "SL",
                      "SN", "SXT", "SYM", "TERZ", "TR", "VOLUNTARY")

# Other (continued, movements, vars, premiere)
others = ("CTD", "MOVT", "MOVTS", "MS", "VAR", "NEW")

# These strings indicate that there's something more complicated going on, manual decoding is needed.
manual_review_needed = ("from", "FROM", "END", "BETWEEN ACTS", "?", "BETWEEN", "etc", "ETC", "ALL SGS IN", "MADE IN",
                        "FROM COLLECTION", "AS PERFORMED AT", "As performed at", "PART", "MUSIC", "AFTER", "PIECE",
                        "SELECTION", "ALSO", "FIRST", "NEVER", "COMPOSED", "RUSH", "[LATER", "EARLIER", "LAST")


class ProgrammeDecoder(object):
    def __init__(self, programme_content):
        # Simple string content of programme
        self.content = programme_content
        # This will contain solely ordered musical pieces with machine-readable content
        self.content_dict = {}
        # This will contain the act breaks, such as (2, 4) - meaning that before the second and the fourth piece there
        # was a break/pause
        self.pauses = ()
        # This will contain solely meta information, such as the conductor, the first violinist etc.
        self.meta_information = {}
        # This will contain everything else, e.g. material directly from the source.
        self.other_infos = {}
        # Split, this will separate out distinct pieces and meta-information such as conductor
        if type(self.content) == float:
            self.content_parts = []
        else:
            # Two subs clean up ; in places where they will split unsplittable information
            self.content = re.sub("(\[[^\]>]+)(;)(.+\])", "\g<1>,\g<3>", self.content)
            self.content = re.sub("(<[^>]+)(;)(.+>)", "\g<1>,\g<3>", self.content)
            # Sometimes forgot to mark end of a piece before a break apparently
            self.content = re.sub("([^;]+)(\d:)", "\g<1>. \g<2>", self.content)
            # Flag programmes for manual review if they contain words that suggest that the content does not entirely
            # follow the usual syntax
            for word in manual_review_needed:
                if word in self.content:
                    self.meta_information["REVIEW"] = [True]
            # Now split the programme into parts, i.e. pieces
            self.content_parts = re.split('; |\. ', self.content)

        # print "Now decoding: ", self.content
        self.decode()
        # print "Content dict: ", self.content_dict
        # print "Pauses: ", self.pauses
        # print "Meta information: ", self.meta_information
        # print "Other information: ", self.other_infos
        # print "\n"

    def __str__(self):
        return "Content: " + str(self.content) + "\n Content dict: " + str(self.content_dict) + \
               "\n Pauses: " + str(self.pauses) + "\n Meta information: " + \
               str(self.meta_information) + "\n Other information: " + str(self.other_infos) + "\n"

    def decode(self):
        # Composer Genre Instrument Performer
        number = 0
        for part in self.content_parts:
            # print number, part

            # Cleans up end of a programme, often denoted by a .
            if part.endswith("."):
                part = part[:-1]

            # Find other interesting information (premieres of pieces...)
            for element in others:
                if element + " " in part:
                    self.meta_information[element] = [True]

            # Find pauses in programmes
            pause = re.match("\s*(1:|2:|3:|4:|5:|6:)\s", part)
            if pause:
                self.pauses += (number,)
                part = re.sub("\s*(1:|2:|3:|4:|5:|6:)\s", "", part)

            # Cleanup of data, materials from sources, i.e. between [] and editorial (referential) <> has to go
            braces_one = re.findall("\[.+\]", part)
            braces_two = re.findall("<.+>", part)
            braces_three = re.findall("\(.+\)", part)
            for braced_item in braces_one:
                self.other_infos[part.replace(braced_item, "").strip()] = [braced_item]
                part = part.replace(braced_item, "")
            for braced_item in braces_two:
                self.other_infos[part.replace(braced_item, "").strip()] = [braced_item]
                part = part.replace(braced_item, "")
            for braced_item in braces_three:
                self.other_infos[part.replace(braced_item, "").strip()] = [braced_item]
                part = part.replace(braced_item, "")
            # More cleanup, annotations like "ALL SGS IN: " have to go
            annotations = re.findall("(\S+:) ", part)
            for annotation in annotations:
                self.other_infos[part.strip()] = [annotation]
                part = part.replace(annotation, "")

            # Remove the from part and put it into own column
            # E.g.: DT 2v MINGOTTI~ RICCIARELLI 'LA_DESTRA' from o ^DEMOFOONTE^
            if "from" in part or "FROM" in part:
                self.content_dict[number] = {}
                self.content_dict[number]["From"] = part.upper().split("FROM")[1].strip()
                part = part.upper().split("FROM")[0]

            regex_on_part = re.match("\s*(\S+) (.+)", part)
            if regex_on_part:
                if regex_on_part.group(1) in all_meta_people:
                    self.meta_information[regex_on_part.group(1).strip()] = regex_on_part.group(2).strip().split()
                # This is sort-of-meta information detailing an instrumentalist/vocalist who won't be mentioned later
                # in the single pieces
                elif regex_on_part.group(1) in all_instruments:
                    self.meta_information[regex_on_part.group(1).strip()] = regex_on_part.group(2).strip().split()
                # Otherwise, this is a "complete piece", i.e. Composer Genre Instrument Performer. Sometimes missing
                # composer.
                else:
                    if number not in self.content_dict:
                        self.content_dict[number] = {}

                    regex_genre_instrument_performer = re.findall("(\S+)", part)
                    ignore = []
                    performer_lock = False
                    for position, information in enumerate(regex_genre_instrument_performer):
                        if position in ignore:
                            continue
                        if str.upper(information) in all_genres_of_music:
                            self.content_dict[number]["Genre"] = str.upper(information).strip()
                        elif str.upper(information) in all_instruments:
                            number_performers = 1
                            if information[0] in ("2", "3", "4", "5", "6"):
                                self.content_dict[number]["Instrument"] = list((information[1:].split()) * int(information[0]))
                                # ignore.append(number)
                                performers = regex_genre_instrument_performer[position + 1:position + 1 + int(information[0])]
                                if len(performers) == int(information[0]):
                                    self.content_dict[number]["Performer"] = performers
                                    performer_lock = True
                                    for i in range(position + 1, position + 1 + int(information[0])):
                                        ignore.append(i)
                                # There's a mismatch between the amount of instruments and the performers specified
                                # e.g. "3V 'THE_FLOCKS'. Hoping that this only occurs like this, i.e. more than one
                                # instrument, but only one performer who then will be multiplied
                                elif len(performers) == 1:
                                    self.content_dict[number]["Performer"] = performers * int(information[0])
                                    performer_lock = True
                                    ignore = [i for i in range(len(regex_genre_instrument_performer))]
                                    self.meta_information["REVIEW"] = [True]
                                # In other cases, throw a "?" in there for manually reviewing that ish
                                else:
                                    self.content_dict[number]["Performer"] = ["?"] * int(information[0])
                                    performer_lock = True
                                    ignore = [i for i in range(len(regex_genre_instrument_performer))]
                                    self.meta_information["REVIEW"] = [True]
                            else:
                                # If followed by another instrument name, there must be the same number of performers
                                for following_information in regex_genre_instrument_performer[position + 1:]:
                                    if str.upper(following_information) in all_instruments:
                                        number_performers += 1
                                    else:
                                        self.content_dict[number]["Instrument"] = \
                                            regex_genre_instrument_performer[position:position + number_performers]
                                        self.content_dict[number]["Performer"] = \
                                            regex_genre_instrument_performer[position + number_performers:position + 2*number_performers]
                                        performer_lock = True
                                        break
                                ignore = [i for i in range(len(regex_genre_instrument_performer))]
                        elif information.startswith("^") and information.endswith("^") \
                             or information.startswith("'") and information.endswith("'"):
                            self.content_dict[number]["Title_of_Piece"] = information.strip()
                        else:
                            if position == 0:
                                self.content_dict[number]["Composer"] = str.upper(information).strip()
                            else:
                                # Otherwise this overwrites. E.g.
                                # DT 2V Gambarini~ + ?
                                # Then ['V', 'V'], ['Gambarini', '+'] the performers are overwritten by '?'
                                if not performer_lock:
                                    self.content_dict[number]["Performer"] = [str.upper(information).strip()]

                    if "Instrument" in self.content_dict[number] and "Performer" in self.content_dict[number]:
                        num_instruments = len(self.content_dict[number]["Instrument"])
                        num_performers = len(self.content_dict[number]["Performer"])
                        if num_instruments != num_performers:
                            if num_instruments < num_performers:
                                self.content_dict[number]["Instrument"] += ["?"] * (num_performers - num_instruments)
                            if num_performers < num_instruments:
                                self.content_dict[number]["Performer"] += ["?"] * (num_instruments - num_performers)
                    number += 1
