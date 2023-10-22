def test_enter_no_more_fifteen_symbols():
    phrase = input('Please enter phrase  no more 15 symbols:  ')
    assert len(phrase) < 15, f"phrase has {len(phrase)} symbols"
