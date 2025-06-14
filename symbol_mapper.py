import pandas as pd

symbol_to_id_map = {}

def load_symbol_map(file_path="data/scrip_master.csv"):
    global symbol_to_id_map
    df = pd.read_csv(file_path, low_memory=False)

    # ✅ Filter only BANKNIFTY options
    df = df[df["SEM_TRADING_SYMBOL"].str.startswith("BANKNIFTY-")]

    # ✅ Build symbol → security_id map
    for _, row in df.iterrows():
        symbol_to_id_map[row["SEM_TRADING_SYMBOL"]] = row["SEM_SMST_SECURITY_ID"]

def get_security_id(tradingsymbol: str) -> str:
    return symbol_to_id_map.get(tradingsymbol)

def get_banknifty_expiry_str():
    """
    Returns expiry string in Dhan format: JUN2025
    """
    today = pd.Timestamp.today()
    return today.strftime("%b").upper() + today.strftime("%Y")

def build_banknifty_symbol(strike: int, option_type: str) -> str:
    expiry = get_banknifty_expiry_str()
    return f"BANKNIFTY-{expiry}-{strike}-{option_type.upper()}"
