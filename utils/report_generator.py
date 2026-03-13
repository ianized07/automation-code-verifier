from analyzers.base import AnalysisResult, Issue


class ReportGenerator:
    @staticmethod
    def generate_text_report(result: AnalysisResult) -> str:
        lines = []
        summary = result.get_summary()
        
        lines.append(f"=== Analysis Report for {summary['language']} ===\n")
        lines.append(f"{'✅' if summary['score'] >= 70 else '⚠️' if summary['score'] >= 40 else '❌'} Overall Score: {summary['score']}/100\n")
        
        if summary['total_issues'] == 0:
            lines.append("🎉 No issues found! Great job!\n")
            return '\n'.join(lines)
        
        # Show all issues comprehensively
        critical = result.get_issues_by_severity(Issue.CRITICAL)
        warnings = result.get_issues_by_severity(Issue.WARNING)
        info = result.get_issues_by_severity(Issue.INFO)
        
        # Detailed score breakdown
        lines.append(f"\n💯 Score Breakdown:")
        lines.append(f"  Starting Score: 100")
        if critical:
            lines.append(f"  Critical Issues ({len(critical)} × -10): -{len(critical) * 10}")
        if warnings:
            lines.append(f"  Warnings ({len(warnings)} × -3): -{len(warnings) * 3}")
        if info:
            lines.append(f"  Info/Suggestions ({len(info)} × -2): -{len(info) * 2}")
        if not result.syntax_valid:
            lines.append(f"  Syntax Error Penalty: -5")
        lines.append(f"  ─────────────────────")
        lines.append(f"  Final Score: {summary['score']}/100")
        
        lines.append(f"\n📊 Issues Summary:")
        lines.append(f"  Total Issues: {summary['total_issues']}")
        lines.append(f"  Critical: {summary['critical']}")
        lines.append(f"  Warnings: {summary['warnings']}")
        lines.append(f"  Info: {summary['info']}")
        
        if critical:
            lines.append(f"\n🔴 CRITICAL ISSUES ({len(critical)}):")
            for issue in critical:
                lines.append(f"  Line {issue.line}: {issue.message}")
                if issue.suggestion:
                    lines.append(f"  💡 {issue.suggestion}")
        
        if warnings:
            lines.append(f"\n⚠️  WARNINGS ({len(warnings)}):")
            for issue in warnings:
                lines.append(f"  Line {issue.line}: {issue.message}")
                if issue.suggestion:
                    lines.append(f"  💡 {issue.suggestion}")
        
        if info:
            lines.append(f"\nℹ️  SUGGESTIONS ({len(info)}):")
            for issue in info:
                lines.append(f"  Line {issue.line}: {issue.message}")
                if issue.suggestion:
                    lines.append(f"  💡 {issue.suggestion}")
        
        return '\n'.join(lines)
    
    @staticmethod
    def generate_html_report(result: AnalysisResult) -> str:
        summary = result.get_summary()
        
        html = f"""
        <div style="font-family: Arial, sans-serif;">
            <h2>Analysis Report for {summary['language']}</h2>
            <h3>Score: {summary['score']}/100</h3>
            <p>Total Issues: {summary['total_issues']}</p>
            <ul>
                <li>Critical: {summary['critical']}</li>
                <li>Warnings: {summary['warnings']}</li>
                <li>Info: {summary['info']}</li>
            </ul>
        </div>
        """
        
        return html
