#!/usr/bin/env python3
"""
@author: Pavel Rojtberg (http://www.rojtberg.net)
@see: https://github.com/paroj/sensors.py
@copyright: The MIT License (MIT) <http://opensource.org/licenses/MIT>
"""
import sensors


def print_feature(chip, feature):
    sfs = list(sensors.SubFeatureIterator(chip, feature))  # get a list of all subfeatures

    label = sensors.get_label(chip, feature)

    skip_name = len(feature.name) + 1  # skip common prefix
    values = [sensors.get_value(chip, sf.number) for sf in sfs]

    if feature.type == sensors.Feature.INTRUSION:
        # short path for INTRUSION to demonstrate type usage
        status = "alarm" if int(values[0]) == 1 else "normal"
        print("\t" + label + "\t" + status)
        return

    names = [sf.name[skip_name:].decode("utf-8") for sf in sfs]
    data = list(zip(names, values))

    str_data = ", ".join([e[0] + ": " + str(e[1]) for e in data])
    print("\t" + label + "\t" + str_data)


if __name__ == "__main__":
    sensors.init()  # optionally takes config file

    print("libsensors version: " + sensors.VERSION)

    for c in sensors.ChipIterator():  # optional arg like "coretemp-*" restricts iterator
        print(sensors.chip_snprintf_name(c) + " (" + sensors.get_adapter_name(c.bus) + ")")
        for f in sensors.FeatureIterator(c):
            print_feature(c, f)

    sensors.cleanup()
