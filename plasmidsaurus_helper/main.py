import argparse
import dnaio
import re


def phred_score_from_char(char):
    ascii_value = ord(char)
    if 33 <= ascii_value <= 126:
        return ascii_value - 33
    else:
        raise ValueError("Invalid Phred character: {}".format(char))


def rev_c(seq):
    """
    simple function that reverse complements a given sequence
    """
    tab = str.maketrans("ACTGNactgn", "TGACNtgacn")
    # first reverse the sequence
    seq = seq[::-1]
    # and then complement
    seq = seq.translate(tab)
    return seq


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input", type=str, help='Input fastq file(s)',
                        required=True, nargs='+')
    parser.add_argument('-o', '--output', type=str, default='auto_rename',
                        required=False, help='Specify custom name for output fasta')
    parser.add_argument('-s', '--start_seq', type=str, default='',
                        help='Optional: add the sequence at the start of your map to help '
                             'alignment. Must be unique! (Aim for 20 nt or so)')
    parser.add_argument('-t','--low_confidence_threshold', default=20,
                        type=int, help='Phred score below which bases will be moved to lower case')
    args = parser.parse_args()

    print(args)

    if len(args.input) > 1:
        assert args.output == 'auto_rename', 'Cannot specify output filename if using multiple inputs!'

    for filename in args.input:
        if args.output == 'auto_rename':
            out_name = filename[:-5] + 'plasmidsaurus_helper.fasta'
        else:
            out_name = args.output

        with dnaio.open(filename) as f:
            for i, record in enumerate(f):
                name = record.name
                seq = record.sequence
                qual = record.qualities

                assert i == 0, 'More than one record found in fastq!'

        # First, convert to lower case based on qualities
        seq2 = ''
        n_low_qual = 0
        for c, q in zip(seq, qual):
            if phred_score_from_char(q) <= args.low_confidence_threshold:
                seq2 += c.lower()
                n_low_qual += 1
            else:
                seq2 += c.upper()

        print(str(n_low_qual) + ' low quality bases found')

        seq2_backup = seq2  # store the original before we mess around...

        for attempt in range(2):
            if attempt == 1:
                # It's possible that the recognition seq crosses the start/end of the seq
                ss_l = len(args.start_seq)
                seq = seq[ss_l:] + seq[:ss_l]
                seq2 = seq2[ss_l:] + seq2[:ss_l]

            # Second, search for matches to the user specified start sequence
            if args.start_seq != '':
                # Convert to upper case and use the upper case sequence
                pattern = re.compile(re.escape(args.start_seq.upper()))

                matches = [match.start() for match in pattern.finditer(seq.upper())]
                rc_matches = [match.start() for match in pattern.finditer(rev_c(seq.upper()))]

                if len(matches) + len(rc_matches) > 1:
                    print('--start_seq is found multiple times, unable to rearrange sequence!')
                    final_seq = seq2_backup

                elif len(matches) + len(rc_matches) == 0:
                    print('--start_seq not found, unable to rearrange sequence!')
                    final_seq = seq2_backup

                elif len(matches) == 1 and len(rc_matches) == 0:
                    print('--start_seq uniquely found, rearranging sequence')
                    final_seq = seq2[matches[0]:] + seq2[:matches[0]]
                    break

                elif len(matches) == 0 and len(rc_matches) == 1:
                    print('--start_seq uniquely found, rearranging sequence')
                    rc_seq2 = rev_c(seq2)
                    final_seq = rc_seq2[rc_matches[0]:] + rc_seq2[:rc_matches[0]]
                    break
            else:
                final_seq = seq2_backup
                break

        with open(out_name, 'w') as file:
            print('Writing out final sequence to ' + out_name)
            file.write(">" + name + "_modified_by_plasmidsaurus_helper" + "\n")
            file.write(final_seq)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()

