// Copyright Oleg Nedbaylo 2020.
// Distributed under the Boost Software License, Version 1.0.
// See accompanying file LICENSE
// or copy at http://www.boost.org/LICENSE_1_0.txt

#pragma once

namespace ssc2ce
{

class Parser{
    public:
    virtual ~Parser() {}

    virtual bool parse(const char *message) = 0;
};

   
} // namespace ssc2ce