import { CommonModule } from '@angular/common';
import { HttpClient, HttpErrorResponse } from '@angular/common/http';
import { Component, inject, signal } from '@angular/core';
import { FormBuilder, ReactiveFormsModule, Validators } from '@angular/forms';

@Component({
  selector: 'app-root',
  imports: [CommonModule, ReactiveFormsModule],
  templateUrl: './app.html',
  styleUrl: './app.css'
})
export class App {
  readonly loading = signal(false);
  readonly error = signal<string | null>(null);
  readonly result = signal<CalculateResponse | null>(null);
  readonly contributionLoading = signal(false);
  readonly contributionError = signal<string | null>(null);
  readonly contributionResult = signal<AnnualContributionResponse | null>(null);

  private readonly fb = inject(FormBuilder);
  private readonly http = inject(HttpClient);

  readonly apiForm = this.fb.group({
    apiBase: ['http://localhost:8000']
  });

  readonly form = this.fb.group({
    retirement_age: [65, [Validators.required, Validators.min(0)]],
    annual_real_return: [0.04, [Validators.required]],
    monthly_drawdown: [2500, [Validators.required, Validators.min(0)]],
    death_age: [90, [Validators.required, Validators.min(1)]]
  });

  readonly annualForm = this.fb.group({
    target_pot: [500000, [Validators.required, Validators.min(0)]],
    starting_pot: [20000, [Validators.required, Validators.min(0)]],
    years_until_retirement: [30, [Validators.required, Validators.min(1)]],
    annual_real_return: [0.04, [Validators.required]]
  });

  submit(): void {
    if (this.form.invalid) {
      this.form.markAllAsTouched();
      return;
    }

    const formValue = this.form.getRawValue();
    const apiBase = (this.apiForm.getRawValue().apiBase ?? '').trim();
    const url = apiBase.length > 0
      ? `${apiBase.replace(/\/$/, '')}/calculate`
      : '/calculate';

    this.loading.set(true);
    this.error.set(null);
    this.result.set(null);

    this.http
      .post<CalculateResponse>(url, {
        retirement_age: formValue.retirement_age,
        annual_real_return: formValue.annual_real_return,
        monthly_drawdown: formValue.monthly_drawdown,
        death_age: formValue.death_age
      })
      .subscribe({
        next: (data) => {
          this.result.set(data);
          this.loading.set(false);
        },
        error: (err: HttpErrorResponse) => {
          this.loading.set(false);
          this.error.set(this.describeError(err));
        }
      });
  }

  submitAnnualContribution(): void {
    if (this.annualForm.invalid) {
      this.annualForm.markAllAsTouched();
      return;
    }

    const formValue = this.annualForm.getRawValue();
    const apiBase = (this.apiForm.getRawValue().apiBase ?? '').trim();
    const url = apiBase.length > 0
      ? `${apiBase.replace(/\/$/, '')}/calculate-annual-contribution`
      : '/calculate-annual-contribution';

    this.contributionLoading.set(true);
    this.contributionError.set(null);
    this.contributionResult.set(null);

    this.http
      .post<AnnualContributionResponse>(url, {
        target_pot: formValue.target_pot,
        starting_pot: formValue.starting_pot,
        years_until_retirement: formValue.years_until_retirement,
        annual_real_return: formValue.annual_real_return
      })
      .subscribe({
        next: (data) => {
          this.contributionResult.set(data);
          this.contributionLoading.set(false);
        },
        error: (err: HttpErrorResponse) => {
          this.contributionLoading.set(false);
          this.contributionError.set(this.describeError(err));
        }
      });
  }

  private describeError(err: HttpErrorResponse): string {
    if (err.status === 0) {
      return 'Unable to reach the API. Check the base URL and CORS settings.';
    }

    const detail = err.error?.detail;
    if (typeof detail === 'string' && detail.trim().length > 0) {
      return detail;
    }

    return `Request failed with status ${err.status}.`;
  }
}

interface CalculateResponse {
  required_pot_at_retirement: number;
  note: string;
}

interface AnnualContributionResponse {
  required_annual_contribution: number;
  note: string;
}
