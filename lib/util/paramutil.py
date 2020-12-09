import argparse
import os

from pyhocon import ConfigFactory


def process_basic_params(parser, logger, core=None):
    parser.add_argument('config', metavar='CONF', type=str, help="Configuration file")
    parser.add_argument('--dbname', dest='dbname', type=str, help="Override db name")
    parser.add_argument('--verbose', action='store_true', help="Set level to verbose")

    args = parser.parse_args()

    conf = ConfigFactory.parse_file(args.config)

    logger.setLevel('INFO')

    if core:
        core.logger.setLevel('INFO')

    if args.verbose:
        logger.setLevel('DEBUG')
        if core:
            core.logger.setLevel('DEBUG')

    if args.dbname:
        os.environ["ARANGODB_DBNAME"] = args.dbname

    return args, conf
