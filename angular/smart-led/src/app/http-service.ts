import { Injectable } from '@angular/core';
import { environment } from 'src/environments/environment.prod';
import { HttpClient, HttpHeaders, HttpErrorResponse } from '@angular/common/http';

@Injectable({
  providedIn: 'root'
})
export class HttpService {
  private serverIp = environment.serverIp;
  private baseUrl = 'http://' + this.serverIp + ':' + environment.serverPort + '/';
  private httpOptions = {
    headers: new HttpHeaders({
      'Content-Type': 'application/json'
    })
  };

  constructor(private httpClient: HttpClient) { }

  public get(relativeUrl: string, id?: string): Promise<any> {
    return new Promise<any>((resolve, reject) => {
      let url = this.baseUrl + relativeUrl;
      if (id) {
        url += '/' + id;
      }
      this.httpClient.get(url).subscribe((result: any) => {
        console.log('Got back result ', result);
        resolve(result);
      },
        error => {
          console.error('Failed while executing GET request', error);
          reject(error);
        });
    });
  }

  public put(relativeUrl: string, id: string, body: any): Promise<any> {
    return new Promise<any>((resolve, reject) => {
      const url = this.baseUrl + relativeUrl + '/' + id;
      this.httpClient.put(url, body, this.httpOptions).subscribe((data: any) => {
        console.log('Got back data as result of PUT: ', data);
        resolve(data);
      }, error => {
        console.error('Failed to execute PUT request:', error);
        reject(error);
      });
    });
  }
}
