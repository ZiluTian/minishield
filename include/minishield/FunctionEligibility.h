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
