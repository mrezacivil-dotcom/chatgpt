def run():
    print("BOT STARTED")

    symbols = get_symbols()

    print("SYMBOL COUNT:", len(symbols))

    if not symbols:
        print("❌ NO SYMBOLS -> API ISSUE")
        return

    sent = 0

    for s in symbols[:10]:
        print("ANALYZING:", s)

        signal = analyze(s)

        print("SIGNAL:", signal)

        send_signal(signal)
        sent += 1

        time.sleep(1)

    print("DONE. SENT:", sent)
