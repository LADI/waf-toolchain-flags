# encoding: utf-8
# SPDX-FileCopyrightText: Copyright © 2023 Nedko Arnaudov
# SPDX-FileCopyrightText: Copyright © 2016-2017 Karl Linden
# SPDX-License-Identifier: BSD-2-Clause

class WafToolchainFlags:
    """
    Waf helper class for handling set of CFLAGS
    and related. The flush() method will
    prepend so to allow supplied by (downstream/distro/builder) waf caller flags
    to override the upstream flags in wscript.
    TODO: upstream this or find alternative easy way of doing the same
    """
    def __init__(self, conf):
        """
        :param conf: Waf configuration object
        """
        self.conf = conf
        self.flags = {}
        for x in ('CPPFLAGS', 'CFLAGS', 'CXXFLAGS', 'LINKFLAGS'):
            self.flags[x] = []

    def flush(self):
        """
        Flush flags to the configuration object
        Prepend is used so to allow supplied by
        (downstream/distro/builder) waf caller flags
        to override the upstream flags in wscript.
        """
        for key, val in self.flags.items():
            self.conf.env.prepend_value(key, val)

    def add(self, key, val):
        """
        :param key: Set to add flags to. 'CPPFLAGS', 'CFLAGS', 'CXXFLAGS' or 'LINKFLAGS'
        :param val: string or list of strings
        """
        flags = self.flags[key]
        if isinstance(val, list):
	    #flags.extend(val)
            for x in val:
                if not isinstance(x, str):
                    raise Exception("value must be string or list of strings. ", type(x))
                flags.append(x)
        elif isinstance(val, str):
            flags.append(val)
        else:
            raise Exception("value must be string or list of strings")

    def add_cpp(self, value):
        """
        Add flag or list of flags to CPPFLAGS
        :param value: string or list of strings
        """
        self.add('CPPFLAGS', value)

    def add_c(self, value):
        """
        Add flag or list of flags to CFLAGS
        :param value: string or list of strings
        """
        self.add('CFLAGS', value)

    def add_cxx(self, value):
        """
        Add flag or list of flags to CXXFLAGS
        :param value: string or list of strings
        """
        self.add('CXXFLAGS', value)

    def add_candcxx(self, value):
        """
        Add flag or list of flags to CFLAGS and CXXFLAGS
        :param value: string or list of strings
        """
        self.add_c(value)
        self.add_cxx(value)

    def add_link(self, value):
        """
        Add flag or list of flags to LINKFLAGS
        :param value: string or list of strings
        """
        self.add('LINKFLAGS', value)

    def display(self):
        """
        Print via conf.msg all non-empty flags
        """
        tool_flags = [
            ('C compiler flags',      ['CFLAGS', 'CPPFLAGS']),
            ('C++ compiler flags',    ['CXXFLAGS', 'CPPFLAGS']),
            ('Linker flags',          ['LINKFLAGS', 'LDFLAGS'])
        ]
        for name, vars in tool_flags:
            flags = []
            for var in vars:
                flags += self.conf.all_envs[''][var]
            if flags:
                self.conf.msg(name, repr(flags), color='NORMAL')
