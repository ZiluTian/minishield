#include "minishield/FlatteningPass.h"
#include "minishield/StatsPass.h"
#include "llvm/Passes/PassBuilder.h"
#include "llvm/Plugins/PassPlugin.h"
#include "minishield/CFGAnalyzer.h"

extern "C" LLVM_ATTRIBUTE_WEAK
llvm::PassPluginLibraryInfo llvmGetPassPluginInfo() {
    return {
        LLVM_PLUGIN_API_VERSION,
        "minishield",
        "1.0",
        [](llvm::PassBuilder &PB) {
            PB.registerAnalysisRegistrationCallback(
                [](llvm::FunctionAnalysisManager &AM){
                    AM.registerPass([] {
                        return minishield::CFGAnalyzer();
                    });
            });
            PB.registerPipelineParsingCallback(
                [](llvm::StringRef Name,
                   llvm::FunctionPassManager &FPM,
                   llvm::ArrayRef<llvm::PassBuilder::PipelineElement> InnerPipeline) {
                        if (!InnerPipeline.empty())
                            return false;
                        if (Name == "minishield-flatten")
                            FPM.addPass(minishield::FlatteningPass());
                        else if (Name == "minishield-stats")
                            FPM.addPass(minishield::StatsPass());
                        else
                            return false;
                        return true;
                }        
            );
        }
    };
}
