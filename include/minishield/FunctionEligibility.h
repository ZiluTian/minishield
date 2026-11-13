// Copyright (c) 2026 ZiluTian
//
// MiniShield code is licensed under MIT; see LICENSE.
// The MiniShield books (volume1, volume2, volume3, docs/, PLAN.md) are CC BY-NC 4.0.
#pragma once

#include "llvm/IR/Function.h"
#include <string>

namespace minishield {
    struct EligibilityResult {
        bool eligible = false;
        std::string reason;
    };

    class FunctionEligibility {
    public:
        static EligibilityResult check(const llvm::Function &F);
    };
} // namespace minishield
