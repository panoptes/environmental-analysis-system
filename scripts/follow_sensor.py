#!/usr/bin/env python

from pocs.utils.messaging import PanMessaging


def main(sensor=None, watch_key=None, channel=None, port=6511, format=True, **kwargs):
    sub = PanMessaging.create_subscriber(port)

    while True:
        data = None
        try:
            msg_channel, msg_data = sub.receive_message()
        except KeyError:
            continue
        else:
            if msg_channel != channel:
                continue

            try:
                data = msg_data['data'][sensor]
            except KeyError:
                continue

            if watch_key in data:
                data = data[watch_key]

        if data is not None:
            if format:
                for k, v in data.items():
                    try:
                        print("{}: {:.02f} ".format(k, v), end='')
                    except ValueError:
                        print(k, ': ', v)
                    except TypeError:
                        print(k, ': ', v)

                print("")
            else:
                print(data)


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description="Follow some serial keys.")

    parser.add_argument('sensor', help="Sensor to watch")
    parser.add_argument('--channel', default='environment', help="Which channel to monitor, e.g. environment, weather")
    parser.add_argument('--watch-key', default=None, help="Key to watch, e.g. amps")
    parser.add_argument('--format', default=True, action='store_true', help="Format key/values")

    args = parser.parse_args()

    try:
        main(**vars(args))
    except KeyboardInterrupt:
        print("Stopping...")