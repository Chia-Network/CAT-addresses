from chia.wallet.puzzles.load_clvm import load_clvm

CAT1_MOD = load_clvm("cat.clvm", package_or_requirement=__name__)
CAT2_MOD = load_clvm("cat_v2.clvm", package_or_requirement=__name__)
