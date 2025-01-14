import os
from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    result = {}
    formula = {}
    
    if request.method == "POST":
        try:
            arrival_rate = float(request.form["arrival_rate"])  # Lambda (λ)
            service_rate = float(request.form["service_rate"])  # Mu (μ)

            if service_rate <= arrival_rate:
                result["error"] = "Service rate (μ) must be greater than arrival rate (λ)."
            else:
                # Traffic intensity (ρ)
                utilization = arrival_rate / service_rate
                formula["utilization"] = f"\\rho = \\frac{{\\lambda}}{{\\mu}} = \\frac{{{arrival_rate}}}{{{service_rate}}} = {utilization}"

                # Average number of customers in the system (L)
                avg_customers = utilization / (1 - utilization)
                formula["avg_customers"] = f"L = \\frac{{\\rho}}{{1 - \\rho}} = \\frac{{{utilization}}}{{1 - {utilization}}} = {avg_customers}"

                # Average time spent in the system (W)
                avg_time = avg_customers / arrival_rate
                formula["avg_time"] = f"W = \\frac{{L}}{{\\lambda}} = \\frac{{{avg_customers}}}{{{arrival_rate}}} = {avg_time}"

                # Number of customers in the queue (LQ)
                avg_queue_customers = (utilization ** 2) / (1 - utilization)
                formula["avg_queue_customers"] = f"LQ = \\frac{{\\rho^2}}{{1 - \\rho}} = \\frac{{{utilization}^2}}{{1 - {utilization}}} = {avg_queue_customers}"

                # Average time spent in the queue (WQ)
                avg_queue_time = avg_queue_customers / arrival_rate
                formula["avg_queue_time"] = f"WQ = \\frac{{LQ}}{{\\lambda}} = \\frac{{{avg_queue_customers}}}{{{arrival_rate}}} = {avg_queue_time}"

                result = {
                    "utilization": round(utilization, 4),
                    "avg_customers": round(avg_customers, 4),
                    "avg_time": round(avg_time, 4),
                    "avg_queue_customers": round(avg_queue_customers, 4),
                    "avg_queue_time": round(avg_queue_time, 4),
                    "formulas": formula
                }
        except ValueError:
            result["error"] = "Please enter valid numerical values for λ and μ."

    return render_template("form.html", result=result)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
