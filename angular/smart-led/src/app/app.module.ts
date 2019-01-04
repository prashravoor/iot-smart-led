import { BrowserModule } from "@angular/platform-browser";
import { BrowserAnimationsModule } from "@angular/platform-browser/animations";
import { NgModule } from "@angular/core";
import { FormsModule } from "@angular/forms";
import { MatSlideToggleModule } from "@angular/material/slide-toggle";
import {MatTableModule} from '@angular/material/table';

import { AppRoutingModule } from "./app-routing.module";
import { AppComponent } from "./app.component";
import { HttpClientModule } from "@angular/common/http";
import { OwlDateTimeModule, OwlNativeDateTimeModule } from "ng-pick-datetime";
import { MatButtonModule } from "@angular/material/button";
import { StatsComponent } from './stats/stats.component';

@NgModule({
    declarations: [AppComponent, StatsComponent],
    imports: [
        BrowserModule,
        BrowserAnimationsModule,
        AppRoutingModule,
        HttpClientModule,
        FormsModule,
        MatSlideToggleModule,
        OwlDateTimeModule,
        OwlNativeDateTimeModule,
        MatButtonModule,
        MatTableModule,
    ],
    providers: [],
    bootstrap: [AppComponent]
})
export class AppModule {}
