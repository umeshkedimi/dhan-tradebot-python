import symbol_mapper
import dhan_api

symbol_mapper.load_symbol_map()

symbol = symbol_mapper.build_banknifty_symbol(55500, "PE")
print(f"Symbol: {symbol}")

security_id = symbol_mapper.get_security_id(symbol)
print(f"Security ID: {security_id}")

if security_id:
    ltp = dhan_api.get_quote(security_id)
    print(f"LTP for {symbol}: {ltp}")
else:
    print("❌ Could not resolve security ID")
