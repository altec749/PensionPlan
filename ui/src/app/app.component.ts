import { CommonModule } from "@angular/common";
import { Component } from "@angular/core";
import { FormsModule } from "@angular/forms";

type CalculateResponse = {
  required_pot_at_retirement: number;
  note?: string;
};

@Component({
  selector: "app-root",
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: "./app.component.html",
  styleUrls: ["./app.component.css"],
})
export class AppComponent {
  model = {
    retirement_age: null as number | null,
    annual_real_return: null as number | null,
    monthly_drawdown: null as number | null,
    death_age: 90,
  };
  status = "";
  error = "";
  result: CalculateResponse | null = null;

  async onSubmit(): Promise<void> {
    this.status = "Calculating...";
    this.error = "";
    this.result = null;

    try {
      const response = await fetch("/calculate", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(this.model),
      });
      const data = (await response.json()) as CalculateResponse & {
        detail?: string;
      };
      if (!response.ok) {
        throw new Error(data.detail || "Calculation failed.");
      }
      this.result = data;
      this.status = "Done.";
    } catch (err) {
      const message = err instanceof Error ? err.message : "Calculation failed.";
      this.error = message;
      this.status = "";
    }
  }
}
