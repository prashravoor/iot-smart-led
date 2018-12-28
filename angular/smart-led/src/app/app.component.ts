import { Component, OnInit } from "@angular/core";
import { HttpService } from "./http-service";
import { Led, LedModifyRequest } from "src/model";

@Component({
    selector: "app-root",
    templateUrl: "./app.component.html",
    styleUrls: ["./app.component.scss"]
})
export class AppComponent implements OnInit {
    title = "Smart LED";
    ledId = undefined;
    led: Led = undefined;
    error = undefined;
    ledSwitch = false;
    ledState = "NA";
    public selectedMoment = new Date();
    public time: any;

    constructor(private httpService: HttpService) {}

    ngOnInit() {
        this.init();
    }

    private init(): void {
        this.error = undefined;
        this.ledId = undefined;
        this.httpService
            .get("lights")
            .then(async (data: string[]) => {
                console.log("Got back Leds:", data);
                // Set LED Id to the first one, always
                if (data) {
                    this.ledId = data[0];
                    try {
                        this.error = undefined;
                        this.led = await this.httpService.get("lights", this.ledId);
                        console.log(this.led);
                        this.setLedSwitch();
                    } catch (error) {
                        console.error("Failed to get details of light ", this.ledId, ": ", error);
                        this.error = error;
                    }
                } else {
                    this.error = "No Lights found!";
                }
            })
            .catch(error => {
                console.error("Failed to get all available lights:", error);
                this.error = error;
            });
    }

    public setLedSwitch() {
        if (this.led.state === "ON") {
            this.ledState = "ON";
            this.ledSwitch = true;
        } else {
            this.ledState = "OFF";
            this.ledSwitch = false;
        }
    }

    public async switchToggled() {
        let request: LedModifyRequest = {};
        if (this.ledSwitch === false) {
            request = <LedModifyRequest>{
                switchOnAfter: 0
            };
        } else {
            request = <LedModifyRequest>{
                switchOffAfter: 0
            };
        }

        this.led = await this.httpService.put("lights", this.ledId, request);
        this.setLedSwitch();
    }

    public schedule(): void {
        const diff: number = new Date().getTime() - this.selectedMoment.getTime();
        console.log("Scheduled!", diff);
        const req = {
            switchOnAfter: diff
        };
        this.httpService
            .put("lights", this.ledId, req)
            .then(data => {
                console.log("Scheduled!");
            })
            .catch(error => {
                console.error("Failed to set schedule: ", error);
            });
    }
}
